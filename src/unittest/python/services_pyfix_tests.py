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

__author__ = "Alexander Metzner"

from pyfix import test, after
from pyassert import assert_that
from mockito import mock, verify, unstub, when, any as any_value

import pypiproxy.services

@test
@after(unstub)
def ensure_that_list_available_package_names_delegates_to_hosted_packages_index_and_proxy():
    pypiproxy.services._hosted_packages_index = mock()
    when(pypiproxy.services._hosted_packages_index).list_available_package_names().thenReturn(["spam", "eggs"])
    
    pypiproxy.services._proxy_packages_index = mock()
    when(pypiproxy.services._proxy_packages_index).list_available_package_names().thenReturn(["ham", "salt", "pepper"])

    actual_list = pypiproxy.services.list_available_package_names()

    assert_that(actual_list).is_equal_to(["eggs", "ham", "pepper", "salt", "spam"])

    verify(pypiproxy.services._hosted_packages_index).list_available_package_names()
    verify(pypiproxy.services._proxy_packages_index).list_available_package_names()


@test
@after(unstub)
def ensure_that_list_versions_delegates_to_hosted_packages_index_when_package_is_hosted():
    pypiproxy.services._hosted_packages_index = mock()
    when(pypiproxy.services._hosted_packages_index).contains("spam").thenReturn(True)

    pypiproxy.services.list_versions("spam")

    verify(pypiproxy.services._hosted_packages_index).contains("spam")
    verify(pypiproxy.services._hosted_packages_index).list_versions("spam")


@test
@after(unstub)
def ensure_that_list_versions_delegates_to_hosted_packages_index_when_package_not_hosted():
    pypiproxy.services._proxy_packages_index = mock()
    pypiproxy.services._hosted_packages_index = mock()
    when(pypiproxy.services._hosted_packages_index).contains("spam").thenReturn(False)

    pypiproxy.services.list_versions("spam")

    verify(pypiproxy.services._hosted_packages_index).contains("spam")
    verify(pypiproxy.services._proxy_packages_index).list_versions("spam")


@test
@after(unstub)
def ensure_that_get_package_content_delegates_to_hosted_packages_index():
    pypiproxy.services._hosted_packages_index = mock()
    package_content = mock()
    when(pypiproxy.services._hosted_packages_index).get_package_content(any_value(), any_value()).thenReturn(package_content)
    when(pypiproxy.services._hosted_packages_index).contains(any_value(), any_value()).thenReturn(True)

    actual_content = pypiproxy.services.get_package_content("spam", "0.1.1")

    assert_that(actual_content).is_equal_to(package_content)
    verify(pypiproxy.services._hosted_packages_index).get_package_content("spam", "0.1.1")


@test
@after(unstub)
def ensure_that_get_package_content_checks_if_package_is_hosted():
    pypiproxy.services._hosted_packages_index = mock()
    when(pypiproxy.services._hosted_packages_index).contains(any_value(), any_value()).thenReturn(True)

    pypiproxy.services.get_package_content("spam", "0.1.1")

    verify(pypiproxy.services._hosted_packages_index).contains("spam", "0.1.1")


@test
@after(unstub)
def ensure_that_get_package_content_uses_proxy_if_package_not_hosted():
    pypiproxy.services._hosted_packages_index = mock()
    pypiproxy.services._proxy_packages_index = mock()
    package_content = mock()
    when(pypiproxy.services._proxy_packages_index).get_package_content(any_value(), any_value()).thenReturn(package_content)
    when(pypiproxy.services._hosted_packages_index).contains(any_value(), any_value()).thenReturn(False)

    actual_content = pypiproxy.services.get_package_content("spam", "0.1.1")

    assert_that(actual_content).is_equal_to(package_content)
    verify(pypiproxy.services._proxy_packages_index).get_package_content("spam", "0.1.1")


@test
@after(unstub)
def ensure_that_add_package_delegates_to_hosted_packages_index():
    pypiproxy.services._hosted_packages_index = mock()

    pypiproxy.services.add_package("spam", "0.1.1", "any_buffer")

    verify(pypiproxy.services._hosted_packages_index).add_package("spam", "0.1.1", "any_buffer")


@test
@after(unstub)
def ensure_that_get_package_statistics_delegates_to_hosted_packages_index():
    pypiproxy.services._hosted_packages_index = mock()
    when(pypiproxy.services._hosted_packages_index).count_packages().thenReturn(0)

    actual = pypiproxy.services.get_package_statistics()

    assert_that(actual).is_equal_to((0, 0))

    verify(pypiproxy.services._hosted_packages_index).list_available_package_names()
    verify(pypiproxy.services._hosted_packages_index).count_packages()
