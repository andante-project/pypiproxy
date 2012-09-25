__author__ = "Alexander Metzner"

import os

from pyassert import Matcher, register_matcher

@register_matcher("is_a_directory")
class DirectoryExistsMatcher (Matcher):
    def accepts(self, actual):
        return isinstance(actual, basestring)

    def describe(self, actual):
        return "'{0}' is not an existing directory".format(actual)

    def matches(self, actual):
        return os.path.exists(actual) and os.path.isdir(actual)