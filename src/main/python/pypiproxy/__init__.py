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

__version__ = "${version}"

import logging

from .configuration import Configuration
from .services import initialize_services

def initialize(config_file):
    configuration = Configuration(config_file)
    initialize_logging(configuration.log_file)
    initialize_services(configuration.packages_directory, configuration.pypi_url)


def initialize_logging(log_file):
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s'")

    log_file_handler = logging.FileHandler(log_file)
    log_file_handler.setLevel(logging.DEBUG)
    log_file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    pypiproxy_logger = logging.getLogger("pypiproxy")
    pypiproxy_logger.setLevel(logging.DEBUG)
    pypiproxy_logger.addHandler(log_file_handler)
    pypiproxy_logger.addHandler(console_handler)

    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.addHandler(log_file_handler)
    werkzeug_logger.addHandler(console_handler)
