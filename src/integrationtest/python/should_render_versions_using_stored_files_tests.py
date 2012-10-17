from integrationtestsupport import download
from liveserver import LiveServer
from pyassert import assert_that
from pyfix import test, run_tests

@test
def integration_test_with_hosted_files():
    with LiveServer() as liveserver:
        liveserver.touch_hosted_file("pyassert-0.1.2.tar.gz")
        liveserver.touch_hosted_file("pyassert-1.2.3.tar.gz")
        liveserver.touch_hosted_file("pyassert-2.3.4.tar.gz")

        index_page = download(liveserver.url + "simple/pyassert/")

        assert_that(index_page).contains("0.1.2").contains("1.2.3").contains("2.3.4")


@test
def integration_test_with_cached_files():
    with LiveServer() as liveserver:
        liveserver.touch_cached_file("pyassert-0.1.2.tar.gz")
        liveserver.touch_cached_file("pyassert-1.2.3.tar.gz")
        liveserver.touch_cached_file("pyassert-2.3.4.tar.gz")

        index_page = download(liveserver.url + "simple/pyassert/")

        assert_that(index_page).contains("0.1.2").contains("1.2.3").contains("2.3.4")

@test
def integration_test_with_hosted_and_cached_files():
    with LiveServer() as liveserver:
        liveserver.touch_cached_file("pyassert-9.8.5.tar.gz")
        liveserver.touch_cached_file("pyassert-8.7.4.tar.gz")
        liveserver.touch_cached_file("pyassert-7.6.5.tar.gz")
        liveserver.touch_hosted_file("pyassert-0.1.2.tar.gz")
        liveserver.touch_hosted_file("pyassert-1.2.3.tar.gz")
        liveserver.touch_hosted_file("pyassert-2.3.4.tar.gz")

        index_page = download(liveserver.url + "simple/pyassert/")

        assert_that(index_page).contains("0.1.2").contains("1.2.3").contains("2.3.4")\
            .does_not_contain("9.8.7").does_not_contain("8.7.6").does_not_contain("7.6.5")


if __name__=='__main__':
    run_tests()
