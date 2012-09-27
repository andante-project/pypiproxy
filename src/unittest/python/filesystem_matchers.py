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
