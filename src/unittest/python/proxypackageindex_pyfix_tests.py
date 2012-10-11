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

__author__ = "Michael Gruber"

from pyfix import after, test, given
from pyfix.fixtures import TemporaryDirectoryFixture
from pyassert import assert_that
from mockito import when, mock, unstub, verify, any as any_value


from pypiproxy.packageindex import ProxyPackageIndex
import pypiproxy.packageindex

@test
@given(temp_dir=TemporaryDirectoryFixture)
def ensure_proxy_checks_if_package_is_already_cached (temp_dir):
    temp_dir.create_directory("packages")
    proxy_package_index = ProxyPackageIndex("cached", temp_dir.join("packages"), "http://pypi.python.org")
    proxy_package_index._package_index = mock()
    when(proxy_package_index._package_index).contains(any_value(), any_value()).thenReturn(True)

    proxy_package_index.get_package_content("pyassert", "0.2.5")

    verify(proxy_package_index._package_index).contains("pyassert", "0.2.5")

@test
@given(temp_dir=TemporaryDirectoryFixture)
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
    when(pypiproxy.packageindex.urllib2).urlopen(any_value()).thenReturn(package_stream)
    when(proxy_package_index._package_index).contains(any_value(), any_value()).thenReturn(False)

    proxy_package_index.get_package_content("pyassert", "0.2.5")

    verify(pypiproxy.packageindex.urllib2).urlopen("http://pypi.python.org/packages/source/p/pyassert/pyassert-0.2.5.tar.gz")
    verify(proxy_package_index._package_index).add_package("pyassert", "0.2.5", package_stream)

if __name__ == "__main__":
    from pyfix import run_tests

    run_tests()
