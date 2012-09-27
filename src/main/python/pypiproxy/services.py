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

from .packageindex import PackageIndex

_hosted_packages_index = PackageIndex("hosted", "packages/hosted")

def list_available_package_names():
    """
        @return: iterable of strings
    """
    return _hosted_packages_index.list_available_package_names()


def list_versions(name):
    """
        @return: iterable of strings
    """
    return _hosted_packages_index.list_versions(name)


def get_package_content(name, version):
    """
        @return: a file-like object
    """
    return _hosted_packages_index.get_package_content(name, version)


def upload_package(name, version, content_stream):
    _hosted_packages_index.add_package(name, version, content_stream)
