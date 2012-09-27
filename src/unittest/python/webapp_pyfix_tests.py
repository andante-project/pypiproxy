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

import StringIO

from pyfix import test, run_tests, after, Fixture, given
from pyassert import assert_that
from mockito import when, verify, never, any as any_value, unstub

from pypiproxy import webapp


class FlaskWebAppFixture(Fixture):
    def provide(self):
        webapp.application.config["TESTING"] = True
        return [webapp.application.test_client()]


@test
@given(web_application=FlaskWebAppFixture)
@after(unstub)
def should_return_list_of_available_package_versions(web_application):
    when(webapp).list_versions(any_value()).thenReturn(["0.1.2", "0.1.3"])
    when(webapp).render_template(any_value(), package_name=any_value(), versions_list=any_value()).thenReturn(
        "rendered template")

    response = web_application.get("/simple/committer/")

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).is_equal_to("rendered template")

    verify(webapp).list_versions("committer")
    verify(webapp).render_template("version-list.html", package_name="committer", versions_list=["0.1.2", "0.1.3"])


@test
@given(web_application=FlaskWebAppFixture)
@after(unstub)
def should_return_error_when_no_versions_available(web_application):
    when(webapp).list_versions(any_value()).thenReturn([])
    when(webapp).render_template(any_value(), package_name=any_value(), versions_list=any_value()).thenReturn(
        "rendered template")

    response = web_application.get("/simple/committer/")

    assert_that(response.status_code).is_equal_to(404)

    verify(webapp).list_versions("committer")
    verify(webapp, never).render_template("version-list.html", package_name=any_value(), versions_list=any_value())


@test
@given(web_application=FlaskWebAppFixture)
@after(unstub)
def should_return_list_of_available_packages(web_application):
    when(webapp).list_available_package_names().thenReturn(["abc", "def", "ghi"])
    when(webapp).render_template(any_value(), package_name_list=any_value()).thenReturn("rendered template")

    response = web_application.get("/simple/")

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).is_equal_to("rendered template")

    verify(webapp).list_available_package_names()
    verify(webapp).render_template("package-list.html", package_name_list=["abc", "def", "ghi"])


@test
@given(web_application=FlaskWebAppFixture)
@after(unstub)
def should_return_package_content(web_application):
    when(webapp).get_package_content(any_value(), any_value()).thenReturn("package content")

    response = web_application.get("/package/package_name/version/package_name-version.tar.gz")

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).is_equal_to("package content")
    assert_that(response.headers.get("Content-Disposition", None)).is_equal_to(
        "attachment; filename=package_name-version.tar.gz")
    assert_that(response.headers.get("Content-Type", None)).is_equal_to(
        "application/x-gzip")

    verify(webapp).get_package_content("package_name", "version")


@test
@given(web_application=FlaskWebAppFixture)
@after(unstub)
def should_send_not_found_when_trying_to_get_package_content_for_nonexisting_package(web_application):
    when(webapp).get_package_content(any_value(), any_value()).thenReturn(None)

    response = web_application.get("/package/package_name/version/package_name-version.tar.gz")

    assert_that(response.status_code).is_equal_to(404)

    verify(webapp).get_package_content("package_name", "version")


@test
@given(web_application=FlaskWebAppFixture)
@after(unstub)
def should_send_bad_request_when_trying_to_upload_package_when_action_is_missing(web_application):
    response = web_application.post("/")
    assert_that(response.status_code).is_equal_to(400)


@test
@given(web_application=FlaskWebAppFixture)
@after(unstub)
def should_send_bad_request_when_trying_to_upload_package_when_name_is_missing(web_application):
    response = web_application.post("/", data={":action": "spam"})
    assert_that(response.status_code).is_equal_to(400)


@test
@given(web_application=FlaskWebAppFixture)
@after(unstub)
def should_send_bad_request_when_trying_to_upload_package_when_version_is_missing(web_application):
    response = web_application.post("/", data={":action": "spam", "name": "spam"})
    assert_that(response.status_code).is_equal_to(400)


@test
@given(web_application=FlaskWebAppFixture)
@after(unstub)
def should_send_bad_request_when_trying_to_upload_package_with_wrong_action(web_application):
    response = web_application.post("/", data={":action": "spam", "name": "name", "version": "version"})
    assert_that(response.status_code).is_equal_to(400)


@test
@given(web_application=FlaskWebAppFixture)
@after(unstub)
def should_send_bad_request_when_trying_to_upload_package_and_content_is_missing(web_application):
    response = web_application.post("/", data={":action": "file_upload", "name": "name", "version": "version"})
    assert_that(response.status_code).is_equal_to(400)


@test
@given(web_application=FlaskWebAppFixture)
@after(unstub)
def should_send_ok_and_delegate_to_services_when_uploading_file(web_application):
    when(webapp).upload_package(any_value(), any_value(), any_value()).thenReturn(None)

    response = web_application.post("/",
        data={":action": "file_upload", "name": "name", "version": "version",
              "content": (StringIO.StringIO("content"), "name-version.tar.gz")})

    assert_that(response.status_code).is_equal_to(200)

    verify(webapp).upload_package("name", "version", "content")


if __name__ == "__main__":
    run_tests()
