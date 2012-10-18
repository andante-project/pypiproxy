import logging
import os
from pyassert import assert_that
from pyfix import test
from pypiproxy import initialize
from pypiproxy.configuration import Configuration



@test
def should_initialize_logging():
    log_statement = "some log statement"
    test_config_file = "src/unittest/resources/pypiproxy_unittest.cfg"
    log_file = Configuration(test_config_file).log_file
    try:
        os.remove(log_file)
    except:
        pass


    initialize(test_config_file)
    pypiproxy_logger = logging.getLogger("pypiproxy")
    pypiproxy_logger.info(log_statement)


    assert_that(log_file).is_a_file()
    with open(log_file) as file_stream:
        assert_that(file_stream.read()).contains(log_statement)

if __name__ == '__main__':
    from pyfix import run_tests

    run_tests()
