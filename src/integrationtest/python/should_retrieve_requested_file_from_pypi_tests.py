from integrationtestsupport import download
from liveserver import LiveServer
from pyassert import assert_that
from pyfix import test, run_tests
from staticpypi import StaticPyPiServer

@test
def integration_test():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            actual_content = download(liveserver.url + "package/yadt/1.2.3/yadt-1.2.3.tar.gz")

            assert_that(actual_content).is_equal_to("static content")

@test
def integration_test_with_hosted_file():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            liveserver.create_hosted_file("yadt-1.2.3.tar.gz")

            actual_content = download(liveserver.url + "package/yadt/1.2.3/yadt-1.2.3.tar.gz")

            assert_that(actual_content).is_equal_to("hosted content")


@test
def integration_test_with_cached_file():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            liveserver.create_cached_file("yadt-1.2.3.tar.gz")

            actual_content = download(liveserver.url + "package/yadt/1.2.3/yadt-1.2.3.tar.gz")

            assert_that(actual_content).is_equal_to("cached content")


@test
def integration_test_with_cached_and_hosted_file():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            liveserver.create_cached_file("yadt-1.2.3.tar.gz")
            liveserver.create_hosted_file("yadt-1.2.3.tar.gz")

            actual_content = download(liveserver.url + "package/yadt/1.2.3/yadt-1.2.3.tar.gz")

            assert_that(actual_content).is_equal_to("hosted content")


if __name__=='__main__':
    run_tests()
