#   pypiproxy
#   Copyright 2012 Michael Gruber, Alexander Metzner
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

__author__ = "Michael Gruber, Maximilien Riehl"

from pyfix import after, test, given
from pyfix.fixtures import TemporaryDirectoryFixture
from pyassert import assert_that
from mockito import when, mock, unstub, verify, any as any_value
from StringIO import StringIO
from urllib2 import URLError

from pypiproxy.packageindex import ProxyPackageIndex
import pypiproxy.packageindex

@test
@given(temp_dir=TemporaryDirectoryFixture)
@after(unstub)
def ensure_proxy_checks_if_package_is_already_cached (temp_dir):
    temp_dir.create_directory("packages")
    proxy_package_index = ProxyPackageIndex("cached", temp_dir.join("packages"), "http://pypi.python.org")
    proxy_package_index._package_index = mock()
    when(proxy_package_index._package_index).contains(any_value(), any_value()).thenReturn(True)

    proxy_package_index.get_package_content("pyassert", "0.2.5")

    verify(proxy_package_index._package_index).contains("pyassert", "0.2.5")

@test
@given(temp_dir=TemporaryDirectoryFixture)
@after(unstub)
def ensure_proxy_gets_package_content_from_package_index_if_it_is_already_cached (temp_dir):
    temp_dir.create_directory("packages")
    proxy_package_index = ProxyPackageIndex("cached", temp_dir.join("packages"), "http://pypi.python.org")
    proxy_package_index._package_index = mock()
    when(proxy_package_index._package_index).contains(any_value(), any_value()).thenReturn(True)

    proxy_package_index.get_package_content("pyassert", "0.2.5")

    verify(proxy_package_index._package_index).get_package_content("pyassert", "0.2.5")

@test
@given(temp_dir=TemporaryDirectoryFixture)
@after(unstub)
def ensure_proxy_gets_package_content_from_pypi_if_it_is_not_cached (temp_dir):
    temp_dir.create_directory("packages")
    proxy_package_index = ProxyPackageIndex("cached", temp_dir.join("packages"), "http://pypi.python.org")
    proxy_package_index._package_index = mock()
    package_stream = mock()
    package_content = mock()
    stream_content = mock()
    when(pypiproxy.packageindex.urllib2).urlopen(any_value()).thenReturn(package_stream)
    when(proxy_package_index._package_index).contains(any_value(), any_value()).thenReturn(False)
    when(proxy_package_index._package_index).get_package_content(any_value(), any_value()).thenReturn(package_content)
    when(package_stream).read().thenReturn(stream_content)

    actual_package = proxy_package_index.get_package_content("pyassert", "0.2.5")

    assert_that(actual_package).is_equal_to(package_content)
    verify(proxy_package_index._package_index).get_package_content("pyassert", "0.2.5")
    verify(pypiproxy.packageindex.urllib2).urlopen("http://pypi.python.org/packages/source/p/pyassert/pyassert-0.2.5.tar.gz")
    verify(proxy_package_index._package_index).add_package("pyassert", "0.2.5", stream_content)

@test
@given(temp_dir=TemporaryDirectoryFixture)
@after(unstub)
def ensure_list_available_package_names_retrieves_index_from_pypi (temp_dir):
    proxy_package_index = ProxyPackageIndex("cached", temp_dir.join("packages"), "http://pypi.python.org")
    package_stream = StringIO("""<!doctype html><html><body>
<a href='alpha'>alpha</a><br/>
<a href='beta'>beta</a><br/>
<a href='gamma'>gamma</a><br/>
</body></html>""")
    when(pypiproxy.packageindex.urllib2).urlopen(any_value()).thenReturn(package_stream)

    actual_list = proxy_package_index.list_available_package_names()

    assert_that(actual_list).is_equal_to(['alpha', 'beta', 'gamma'])
    verify(pypiproxy.packageindex.urllib2).urlopen("http://pypi.python.org/simple/")

@test
@given(temp_dir=TemporaryDirectoryFixture)
@after(unstub)
def ensure_list_available_package_names_delegates_to_cached_index_when_failing_to_download_index (temp_dir):
    proxy_package_index = ProxyPackageIndex("cached", temp_dir.join("packages"), "http://pypi.python.org")
    temp_dir.touch("packages", "spam-0.1.2.tar.gz")
    temp_dir.touch("packages", "eggs-0.1.2.tar.gz")
    when(pypiproxy.packageindex.urllib2).urlopen(any_value()).thenRaise(URLError("Failed!"))

    actual_list = proxy_package_index.list_available_package_names()

    assert_that(actual_list).is_equal_to(['eggs', 'spam'])

@test
@given(temp_dir=TemporaryDirectoryFixture)
@after(unstub)
def ensure_list_versions_retrieves_versions_from_pypi (temp_dir):
    proxy_package_index = ProxyPackageIndex("cached", temp_dir.join("packages"), "http://pypi.python.org")
    package_stream = StringIO("""<!doctype html><html><body>
<a href='package-0.1.2.tar.gz'>package-0.1.2.tar.gz</a><br/>
<a href='package-1.2.3.tar.gz'>package-1.2.3.tar.gz</a><br/>
<a href='package-1.2.3.egg'>package-1.2.3.egg</a><br/>
<a href='package-2.3.4.egg'>package-2.3.4.egg</a><br/>
<a href='package-2.3.4.tar.gz'>package-2.3.4.tar.gz</a><br/>
</body></html>""")
    when(pypiproxy.packageindex.urllib2).urlopen(any_value()).thenReturn(package_stream)

    actual_list = proxy_package_index.list_versions("package")

    assert_that(actual_list).is_equal_to(['0.1.2', '1.2.3', '2.3.4'])
    verify(pypiproxy.packageindex.urllib2).urlopen("http://pypi.python.org/simple/package/")

@test
@given(temp_dir=TemporaryDirectoryFixture)
@after(unstub)
def ensure_list_versions_delegates_to_cached_versions_when_to_download_versions_from_pypi (temp_dir):
    proxy_package_index = ProxyPackageIndex("cached", temp_dir.join("packages"), "http://pypi.python.org")
    temp_dir.touch("packages", "spam-0.1.2.tar.gz")
    temp_dir.touch("packages", "spam-2.3.4.tar.gz")
    temp_dir.touch("packages", "spam-2.3.4.egg")
    temp_dir.touch("packages", "spam-1.2.3.tar.gz")
    temp_dir.touch("packages", "eggs-0.1.2.tar.gz")
    temp_dir.touch("packages", "eggs-0.1.2.egg")
    when(pypiproxy.packageindex.urllib2).urlopen(any_value()).thenRaise(URLError("Failed!"))

    actual_list = proxy_package_index.list_versions("spam")

    assert_that(actual_list).is_equal_to(['0.1.2', '1.2.3', '2.3.4'])
    verify(pypiproxy.packageindex.urllib2).urlopen("http://pypi.python.org/simple/spam/")

if __name__ == "__main__":
    from pyfix import run_tests

    run_tests()
