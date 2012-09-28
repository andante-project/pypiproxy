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

import ConfigParser

class Configuration(object):
    SECTION = "pypiproxy"
    OPTION_LOG_FILE = "log_file"
    OPTION_PACKAGES_DIRECTORY = "packages_directory"

    DEFAULT_LOG_FILE = "/var/log/pypiproxy.log"

    def __init__(self, config_file_name):
        self._config_parser = ConfigParser.RawConfigParser()
        self._load_config_file(config_file_name)

        self._verify_config()

    def _get_option(self, option, default_value=None):
        if not self._config_parser.has_option(Configuration.SECTION, option):
            if default_value:
                return default_value
            raise ValueError("Missing configuration option '%s' in section '%s'", option, Configuration.SECTION)
        return self._config_parser.get(Configuration.SECTION, option)

    @property
    def log_file(self):
        return self._get_option(Configuration.OPTION_LOG_FILE, Configuration.DEFAULT_LOG_FILE)

    @property
    def packages_directory(self):
        return self._get_option(Configuration.OPTION_PACKAGES_DIRECTORY)

    def _load_config_file(self, config_file_name):
        try:
            if self._config_parser.read(config_file_name) != [config_file_name]:
                raise ValueError("Failed to load config file '{0}'".format(config_file_name))
        except ConfigParser.Error as e:
            raise ValueError("Error loading config file: {0}".format(e))


    def _verify_config(self):
        if not self._config_parser.has_section(Configuration.SECTION):
            raise ValueError("Invalid config file: No such section '{0}'".format(Configuration.SECTION))
