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

__author__ = "Michael Gruber, Alexander Metzner"

from pyfix import test, run_tests
from pyassert import assert_that
from mockito import when, verify, never, any as any_value, unstub

from pypiproxy import webapp


@test
def should_return_list_of_available_package_versions():
    when(webapp).list_versions(any_value()).thenReturn(["0.1.2", "0.1.3"])
    when(webapp).render_template(any_value(), package_name=any_value(), versions_list=any_value()).thenReturn("rendered template")

    actual_result = webapp.handle_version_list("committer")
    
    assert_that(actual_result).is_equal_to("rendered template")

    verify(webapp).list_versions("committer")
    verify(webapp).render_template("version-list.html", package_name="committer", versions_list=["0.1.2", "0.1.3"])
    unstub()

@test
def should_return_error_when_no_versions_available():
    when(webapp).list_versions(any_value()).thenReturn([])
    when(webapp).render_template(any_value(), package_name=any_value(), versions_list=any_value()).thenReturn("rendered template")

    actual_result = webapp.handle_version_list("committer")
    
    assert_that(actual_result).is_equal_to(("",404))

    verify(webapp).list_versions("committer")
    verify(webapp, never).render_template("version-list.html", package_name=any_value(), versions_list=any_value())
    unstub()

@test
def should_return_list_of_available_packages():
    when(webapp).list_available_package_names().thenReturn(["abc", "def", "ghi"])
    when(webapp).render_template(any_value(), package_name_list=any_value()).thenReturn("rendered template")
    
    actual_result = webapp.handle_package_list()

    assert_that(actual_result).is_equal_to("rendered template")
    
    verify(webapp).list_available_package_names()
    verify(webapp).render_template("package-list.html", package_name_list=["abc", "def", "ghi"])
    unstub()


@test
def should_return_package_content():
    when(webapp).get_package_content(any_value(), any_value()).thenReturn("package content")
    
    actual_content = webapp.handle_package_content("package_name", "version", "package_name-version.tar.gz")
    
    assert_that(actual_content).is_equal_to("package content")
    
    verify(webapp).get_package_content("package_name", "version")
    
    
if __name__ == "__main__":
    run_tests()
