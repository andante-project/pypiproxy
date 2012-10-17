from pyassert import assert_that
from pyfix import after, before, given, test, run_tests
from liveserver import LiveServer
from integrationtestsupport import upload
from httplib import OK

@test
def integration_test():
    with LiveServer() as liveserver:
        status_code = upload().file("schnulli.tar.gz").file_content("Hello world").package_name("foobar").package_version("1.0.0").to(liveserver)

        assert_that(status_code).is_equal_to(OK)
        assert_that("target/packages_integrationtest/hosted/foobar-1.0.0.tar.gz").is_a_file()

if __name__=='__main__':
    run_tests()
