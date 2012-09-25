__author__ = "Alexander Metzner"

from pyfix import test
from mockito import mock, verify

import pypiproxy.services

@test
def ensure_that_list_available_package_names_delegates_to_hosted_packages_index():
    pypiproxy.services._hosted_packages_index = mock()

    pypiproxy.services.list_available_package_names()

    verify(pypiproxy.services._hosted_packages_index).list_available_package_names()


@test
def ensure_that_list_versions_delegates_to_hosted_packages_index():
    pypiproxy.services._hosted_packages_index = mock()

    pypiproxy.services.list_versions("spam")

    verify(pypiproxy.services._hosted_packages_index).list_versions("spam")


@test
def ensure_that_get_package_content_to_hosted_packages_index():
    pypiproxy.services._hosted_packages_index = mock()

    pypiproxy.services.get_package_content("spam", "0.1.1")

    verify(pypiproxy.services._hosted_packages_index).get_package_content("spam", "0.1.1")
