__author__ = "Alexander Metzner"

import itertools
import os
import re

_PACKAGE_NAME_AND_VERSION_PATTERN = re.compile(r"^(.*?)(-([0-9.]+.*)).tar.gz$")

def _guess_name_and_version(filename):
    result = _PACKAGE_NAME_AND_VERSION_PATTERN.match(filename)
    return result.group(1), result.group(3)


class PackageIndex(object):
    def __init__(self, name, directory):
        self._name = name
        self._directory = directory

        if not os.path.exists(directory):
            os.makedirs(directory)

    def list_available_package_names(self):
        return UniqueIterator(itertools.imap(lambda name_and_version: name_and_version[0], self._read_packages()))

    def list_versions(self, package):
        return itertools.imap(lambda name_and_version: name_and_version[1],
            itertools.ifilter(lambda name_and_version: name_and_version[0] == package, self._read_packages()))

    def _read_packages(self):
        return itertools.imap(_guess_name_and_version, self._read_files())

    def _read_files(self):
        return itertools.ifilter(lambda f: f.endswith("tar.gz"), os.listdir(self._directory))


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

