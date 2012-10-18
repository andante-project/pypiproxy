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

from pyfix import test, given
from pyfix.fixtures import TemporaryDirectoryFixture
from pyassert import assert_that

from pypiproxy.configuration import Configuration

@test
@given(temp_dir=TemporaryDirectoryFixture)
def constructor_should_raise_exception_when_config_file_does_not_exist(temp_dir):
    def callback():
        Configuration(temp_dir.join("does_not_exist.cfg"))

    assert_that(callback).raises(ValueError)


@test
@given(temp_dir=TemporaryDirectoryFixture)
def constructor_should_raise_exception_when_config_file_has_invalid_content(temp_dir):
    temp_dir.create_file("config.cfg", "spam")

    def callback():
        Configuration(temp_dir.join("config.cfg"))

    assert_that(callback).raises(ValueError)


@test
@given(temp_dir=TemporaryDirectoryFixture)
def constructor_should_raise_exception_when_config_does_not_contain_expected_section(temp_dir):
    temp_dir.create_file("config.cfg", "[spam]\nspam=eggs")

    def callback():
        Configuration(temp_dir.join("config.cfg"))

    assert_that(callback).raises(ValueError)


@test
@given(temp_dir=TemporaryDirectoryFixture)
def should_return_default_log_file_when_no_log_file_option_is_given(temp_dir):
    temp_dir.create_file("config.cfg", "[{0}]".format(Configuration.SECTION))

    config = Configuration(temp_dir.join("config.cfg"))
    assert_that(config.log_file).is_equal_to(Configuration.DEFAULT_LOG_FILE)


@test
@given(temp_dir=TemporaryDirectoryFixture)
def should_return_given_log_file_when_log_file_option_is_given(temp_dir):
    temp_dir.create_file("config.cfg",
        "[{0}]\n{1}=spam.log".format(Configuration.SECTION, Configuration.OPTION_LOG_FILE))

    config = Configuration(temp_dir.join("config.cfg"))
    assert_that(config.log_file).is_equal_to("spam.log")


@test
@given(temp_dir=TemporaryDirectoryFixture)
def should_return_default_pypi_url_when_no_pypi_url_option_is_given(temp_dir):
    temp_dir.create_file("config.cfg", "[{0}]".format(Configuration.SECTION))

    config = Configuration(temp_dir.join("config.cfg"))
    assert_that(config.pypi_url).is_equal_to(Configuration.DEFAULT_PYPI_URL)


@test
@given(temp_dir=TemporaryDirectoryFixture)
def should_return_given_pypi_url_when_pypi_url_option_is_given(temp_dir):
    temp_dir.create_file("config.cfg",
        "[{0}]\n{1}=spam.log".format(Configuration.SECTION, Configuration.OPTION_PYPI_URL))

    config = Configuration(temp_dir.join("config.cfg"))
    assert_that(config.pypi_url).is_equal_to("spam.log")


@test
@given(temp_dir=TemporaryDirectoryFixture)
def should_raise_exception_when_no_hosted_packages_directory_option_is_given_and_directory_is_retrieved(temp_dir):
    temp_dir.create_file("config.cfg", "[{0}]".format(Configuration.SECTION))

    config = Configuration(temp_dir.join("config.cfg"))

    def callback():
        config.hosted_packages_directory

    assert_that(callback).raises(ValueError)

@test
@given(temp_dir=TemporaryDirectoryFixture)
def should_raise_exception_when_no_cached_packages_directory_option_is_given_and_directory_is_retrieved(temp_dir):
    temp_dir.create_file("config.cfg", "[{0}]".format(Configuration.SECTION))

    config = Configuration(temp_dir.join("config.cfg"))

    def callback():
        config.cached_packages_directory

    assert_that(callback).raises(ValueError)


@test
@given(temp_dir=TemporaryDirectoryFixture)
def should_return_given_hosted_packages_directory_when_packages_directory_option_is_given(temp_dir):

    temp_dir.create_file("config.cfg",
        "[{0}]\n{1}=packages/hosted".format(Configuration.SECTION, Configuration.OPTION_HOSTED_PACKAGES_DIRECTORY))

    config = Configuration(temp_dir.join("config.cfg"))
    assert_that(config.hosted_packages_directory).is_equal_to("packages/hosted")


@test
@given(temp_dir=TemporaryDirectoryFixture)
def should_return_given_cached_packages_directory_when_packages_directory_option_is_given(temp_dir):
    temp_dir.create_file("config.cfg",
        "[{0}]\n{1}=packages/cached".format(Configuration.SECTION, Configuration.OPTION_CACHED_PACKAGES_DIRECTORY))

    config = Configuration(temp_dir.join("config.cfg"))
    assert_that(config.cached_packages_directory).is_equal_to("packages/cached")



if __name__ == '__main__':
    from pyfix import run_tests

    run_tests()
