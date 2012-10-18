from integrationtestsupport import download
from liveserver import LiveServer
from pyassert import assert_that
from pyfix import test, run_tests
from staticpypi import StaticPyPiServer

@test
def integration_test():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            index_page = download(liveserver.url + "simple/")

            assert_that(index_page).contains("public-a").contains("public-b").contains("public-c")

@test
def integration_test_with_hosted_file():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            liveserver.create_hosted_file("pyassert-0.1.2.tar.gz")

            index_page = download(liveserver.url + "simple/")

            assert_that(index_page).contains("public-a").contains("public-b").contains("public-c").contains("pyassert")

@test
def integration_test_with_cached_file():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            liveserver.create_cached_file("pyassert-0.1.2.tar.gz")

            index_page = download(liveserver.url + "simple/")

            assert_that(index_page).contains("public-a").contains("public-b").contains("public-c")
            assert_that(index_page).does_not_contain("pyassert")

@test
def integration_test_with_hosted_and_cached_file():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            liveserver.create_cached_file("schnulli-0.1.2.tar.gz")
            liveserver.create_hosted_file("committer-0.0.60.tar.gz")

            index_page = download(liveserver.url + "simple/")

            assert_that(index_page).contains("public-a").contains("public-b").contains("public-c").contains("committer")
            assert_that(index_page).does_not_contain("schnulli")

if __name__=='__main__':
    run_tests()
