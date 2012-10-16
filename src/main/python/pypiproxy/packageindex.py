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

__author__ = "Alexander Metzner, Michael Gruber, Maximilien Riehl"

import itertools
import logging
import glob
import os
import re
import urllib2

LOGGER = logging.getLogger("pypiproxy.packageindex")

_PACKAGE_NAME_AND_VERSION_PATTERN = re.compile(r"^(.*?)(-([0-9.]+.*)).tar.gz$")
_HREF_PATTERN = re.compile(r'href=[\'"]?([^\'" >]+)')

def _guess_name_and_version(filename):
    result = _PACKAGE_NAME_AND_VERSION_PATTERN.match(filename)
    if result:
        return result.group(1), result.group(3)

    filename = filename.replace(r".tar.gz", "")

    if "-" in filename:
        split_index = filename.rfind("-")
        return filename[0:split_index], filename[split_index + 1:]

    raise ValueError("Invalid package file name: '{0}'".format(filename))


class PackageIndex(object):
    FILE_SUFFIX = ".tar.gz"

    def __init__(self, name, directory):
        self._name = name
        self._directory = directory
        LOGGER.info("Creating packageindex '%s' serving directory '%s'", name, self._directory)

        if not os.path.exists(self._directory):
            os.makedirs(self._directory)

    @property
    def directory(self):
        return self._directory

    def add_package(self, name, version, content):
        filename = self._filename_from_name_and_version(name, version)

        LOGGER.info("Adding package {0} in version {1} as file {2}".format(name, version, filename))

        with open(filename, "wb") as package_file:
            package_file.write(content)

    def contains(self, name, version="*"):
        filename = self._filename_from_name_and_version(name, version)
        list_of_files = glob.glob(filename)
        return len(list_of_files) > 0

    def count_packages(self):
        return len([p for p in self._read_packages()])

    def get_package_content(self, package, version):
        filename = os.path.join(self._directory, package + "-" + version + PackageIndex.FILE_SUFFIX)
        if not self.contains(package, version):
            return None

        with open(filename, "rb") as f:
            return f.read()

    def list_available_package_names(self):
        package_names = [p for p in itertools.imap(lambda name_and_version: name_and_version[0], self._read_packages())]
        package_names = sorted(package_names)
        return UniqueIterator(package_names.__iter__())

    def list_versions(self, name):
        LOGGER.info("Listing versions for '{0}'".format(name))

        return itertools.imap(lambda name_and_version: name_and_version[1],
            itertools.ifilter(lambda name_and_version: name_and_version[0] == name, self._read_packages()))

    def _filename_from_name_and_version(self, name, version):
        return os.path.join(self._directory, "{0}-{1}{2}".format(name, version, PackageIndex.FILE_SUFFIX))

    def _read_files(self):
        return itertools.ifilter(lambda f: f.endswith(PackageIndex.FILE_SUFFIX), os.listdir(self._directory))

    def _read_packages(self):
        return itertools.imap(_guess_name_and_version, self._read_files())


class ProxyPackageIndex(object):
    """
    Retrieves the packages from another pypi and stores them in a package index. 
    """
    def __init__(self, name, directory, pypi_url):
        self._package_index = PackageIndex(name, directory)
        self._pypi_url = pypi_url

    def get_package_content(self, name, version):
        if not self._package_index.contains(name, version):
            filename = "{0}-{1}{2}".format(name, version, PackageIndex.FILE_SUFFIX)
            package_url = "{0}/packages/source/{1}/{2}/{3}".format(self._pypi_url, name[0], name, filename)
            LOGGER.info("Downloading package {0} in version {1} from {2}".format(name, version, package_url))
            content = self._fetch_url(package_url, raw=True)

            self._package_index.add_package(name, version, content)

        return self._package_index.get_package_content(name, version)

    def list_available_package_names(self):
        pypi_index_url = "{0}/simple/".format(self._pypi_url)
        LOGGER.info("Downloading index from {0}".format(pypi_index_url))

        index_content = self._fetch_url(pypi_index_url)
        if index_content is not None:
            return self._extract_package_names(index_content)
        else:
            return sorted(list(self._package_index.list_available_package_names()))

    def list_versions(self, name):
        versions_url = "{0}/simple/{1}/".format(self._pypi_url, name)
        LOGGER.info("Downloading versions from {0}".format(versions_url))
        versions_content = self._fetch_url(versions_url)

        if versions_content is not None:
            return self._extract_versions(versions_content)
        else:
            return sorted(list(self._package_index.list_versions(name)))

    def _extract_package_names(self, index_content):
        result = []
        for line in index_content.split('\n'):
            if line.startswith('<a href'):
                name = self._extract_package_name_from_link(line)
                result.append(name)
        return result

    def _extract_package_name_from_link(self, line):
        return line[line.find('>') + 1:line.rfind('</a><br/>')]

    def _extract_versions(self, versions_content):
        result = []
        for line in versions_content.split("\n"):
            line = line.decode("utf8")
            if line.startswith('<a href') and line.find(PackageIndex.FILE_SUFFIX) >= 0:
                name = self._href_from(line)
                if "#md5" in name:
                    name = name[0:name.rfind('#md5')]
                version = _guess_name_and_version(name)[1]
                result.append(version)
        return result

    def _href_from(self, text):
        hrefs = _HREF_PATTERN.findall(text)
        if len(hrefs) is not 1:
            raise ValueError("Invalid link contains multiple href values")
        return hrefs[0]

    def _fetch_url(self, url, raw=False):
        stream = None
        try:
            stream = urllib2.urlopen(url)
            raw_content = stream.read()
            if raw:
                return raw_content
            else:
                return raw_content.decode("utf8")
        except urllib2.URLError as e:
            LOGGER.warn("Could not fetch {0}: {1}".format(url, e))
            return None
        finally:
            if stream is not None:
                stream.close()

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

