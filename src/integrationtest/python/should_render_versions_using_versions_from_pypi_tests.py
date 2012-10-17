from integrationtestsupport import download
from liveserver import LiveServer
from pyassert import assert_that
from pyfix import test, run_tests
from staticpypi import StaticPyPiServer

@test
def integration_test():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            index_page = download(liveserver.url + "simple/yadt/")

            assert_that(index_page).contains("0.1.2").contains("1.2.3").contains("2.3.4")

@test
def integration_test_with_hosted_file():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            liveserver.touch_hosted_file("yadt-5.4.3.tar.gz")

            index_page = download(liveserver.url + "simple/yadt/")

            assert_that(index_page).does_not_contain("0.1.2").does_not_contain("1.2.3").does_not_contain("2.3.4").contains("5.4.3")

@test
def integration_test_with_cached_file():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            liveserver.touch_cached_file("yadt-5.4.3.tar.gz")

            index_page = download(liveserver.url + "simple/yadt/")

            assert_that(index_page).contains("0.1.2").contains("1.2.3").contains("2.3.4").does_not_contain("5.4.3")

@test
def integration_test_with_hosted_and_cached_file():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            liveserver.touch_cached_file("yadt-5.4.3.tar.gz")
            liveserver.touch_hosted_file("yadt-9.8.7.tar.gz")

            index_page = download(liveserver.url + "simple/yadt/")

            assert_that(index_page).contains("9.8.7") \
               .does_not_contain("0.1.2").does_not_contain("1.2.3").does_not_contain("2.3.4").does_not_contain("5.4.3")

if __name__=='__main__':
    run_tests()
