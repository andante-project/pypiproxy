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

import logging

from .packageindex import PackageIndex

LOGGER = logging.getLogger("pypiproxy.services")

_hosted_packages_index = None

def initialize_services(packages_directory):
    global _hosted_packages_index
    _hosted_packages_index = PackageIndex("hosted", packages_directory)


def get_package_statistics():
    """
    Returns a tuple containing several statistics of the index:
    # of package files, # of unique package names
    """
    LOGGER.debug("Calculating package statistics")
    package_names = _hosted_packages_index.list_available_package_names()
    number_of_unique_packages = len([p for p in package_names]) if package_names else 0
    return _hosted_packages_index.count_packages(), number_of_unique_packages


def list_available_package_names():
    """
        @return: iterable of strings
    """
    LOGGER.debug("Listing available packages")
    return _hosted_packages_index.list_available_package_names()


def list_versions(name):
    """
        @return: iterable of strings
    """
    LOGGER.debug("Listing versions for package '%s'", name)
    return _hosted_packages_index.list_versions(name)


def get_package_content(name, version):
    """
        @return: a file-like object
    """
    LOGGER.debug("Retrieving package content for '%s %s'", name, version)

    if not _hosted_packages_index.contains(name, version):
        LOGGER.error("Package {0} of version {1} not hosted.".format(name, version))
        return None

    return _hosted_packages_index.get_package_content(name, version)


def add_package(name, version, content_stream):
    LOGGER.debug("Adding package '%s %s'", name, version)
    _hosted_packages_index.add_package(name, version, content_stream)
