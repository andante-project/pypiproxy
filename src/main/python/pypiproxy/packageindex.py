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

import itertools
import os
import re

_PACKAGE_NAME_AND_VERSION_PATTERN = re.compile(r"^(.*?)(-([0-9.]+.*)).tar.gz$")

def _guess_name_and_version(filename):
    result = _PACKAGE_NAME_AND_VERSION_PATTERN.match(filename)
    return result.group(1), result.group(3)


class PackageIndex(object):
    FILE_SUFFIX = ".tar.gz"

    def __init__(self, name, directory):
        self._name = name
        self._directory = directory

        if not os.path.exists(directory):
            os.makedirs(directory)

    def add_package(self, name, version, content_stream):
        filename = os.path.join(self._directory, "{0}-{1}{2}".format(name, version, PackageIndex.FILE_SUFFIX))
        with open(filename, "wb") as package_file:
            package_file.write(content_stream)

    def list_available_package_names(self):
        return UniqueIterator(itertools.imap(lambda name_and_version: name_and_version[0], self._read_packages()))

    def list_versions(self, package):
        return itertools.imap(lambda name_and_version: name_and_version[1],
            itertools.ifilter(lambda name_and_version: name_and_version[0] == package, self._read_packages()))

    def get_package_content(self, package, version):
        filename = os.path.join(self._directory, package + "-" + version + PackageIndex.FILE_SUFFIX)
        if not os.path.exists(filename):
            return None

        with open(filename, "rb") as f:
            return f.read()

    def _read_packages(self):
        return itertools.imap(_guess_name_and_version, self._read_files())

    def _read_files(self):
        return itertools.ifilter(lambda f: f.endswith(PackageIndex.FILE_SUFFIX), os.listdir(self._directory))


class UniqueIterator(object):
    """
    Iterator that only yields a value if it differs from the value returned before.
    """

    def __init__(self, base_iterator):
        self._base_iterator = base_iterator
        self._last_value = None
        self._started = False

    def __iter__(self):
        return self

    def next(self):
        candidate = self._base_iterator.next()
        if not self._started:
            self._started = True
            self._last_value = candidate
            return candidate

        if self._last_value == candidate:
            return self.next()
        self._last_value = candidate
        return candidate

