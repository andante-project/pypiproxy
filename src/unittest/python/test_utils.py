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

import os
import shutil
import sys
import tempfile

from pyfix import Fixture
from pyassert import Matcher, register_matcher

@register_matcher("is_a_directory")
class DirectoryExistsMatcher(Matcher):
    def accepts(self, actual):
        return isinstance(actual, basestring)

    def describe(self, actual):
        return "'{0}' is not an existing directory".format(actual)

    def matches(self, actual):
        return os.path.exists(actual) and os.path.isdir(actual)


@register_matcher("is_a_file")
class FileExistsMatcher(Matcher):
    def accepts(self, actual):
        return isinstance(actual, basestring)

    def describe(self, actual):
        return "'{0}' is not an existing file".format(actual)

    def matches(self, actual):
        return os.path.exists(actual) and os.path.isfile(actual)


@register_matcher("has_file_length_of")
class FileLengthMatcher(Matcher):
    def __init__(self, expected_size):
        self._expected_size = expected_size

    def accepts(self, actual):
        return isinstance(actual, basestring)

    def describe(self, actual):
        return "Actual '{0}' has a length of {1:d} bytes but expected {2:d} bytes.".format(actual,
            self._get_file_size(actual), self._expected_size)

    def matches(self, actual):
        return int(self._get_file_size(actual)) == int(self._expected_size)

    def _get_file_size(self, filename):
        return os.stat(filename).st_size


@register_matcher("raises")
class RaisesMatcher(Matcher):
    def __init__(self, expected_exception_type):
        self._expected_exception_type = expected_exception_type
        self._actual_exception_type = None

    def matches(self, actual):
        try:
            actual()
        except:
            self._actual_exception_type = sys.exc_info()[0]
        return self._actual_exception_type == self._expected_exception_type

    def describe(self, actual):
        return "Expected '{0}' to raise exception of type {1} but instead caught {2}".format(actual,
            self._expected_exception_type, self._actual_exception_type)


class TempDirHandle(object):
    def __init__(self):
        self.basedir = tempfile.mkdtemp(prefix=__name__)

    def __del__(self):
        if os.path.exists(self.basedir):
            shutil.rmtree(self.basedir)

    def join(self, *path_elements):
        path_elements = [self.basedir] + list(path_elements)
        return os.path.join(*path_elements)

    def touch(self, *path_elements):
        f = open(self.join(*path_elements), "w")
        try:
            f.write("")
        finally:
            f.close()

    def create_directory(self, *path_elements):
        os.makedirs(self.join(*path_elements))

    def create_file(self, name_parts, content, binary=False):
        if isinstance(name_parts, basestring):
            name_parts = [name_parts]
        open_flags = "w" + ("b" if binary else "")

        with open(self.join(*name_parts), open_flags) as f:
            f.write(content)


class TempDirFixture(Fixture):
    def reclaim(self, temp_dir_handle):
        del temp_dir_handle

    def provide(self):
        return [TempDirHandle()]