from integrationtestsupport import download
from liveserver import LiveServer
from pyassert import assert_that
from pyfix import test, run_tests
from staticpypi import StaticPyPiServer

@test
def integration_test_with_hosted_file():
    with LiveServer() as liveserver:
        liveserver.touch_hosted_file("pyassert-0.1.2.tar.gz")

        index_page = download(liveserver.url + "simple/")

        assert_that(index_page).contains("pyassert")

@test
def integration_test_with_cached_file():
    with LiveServer() as liveserver:
        liveserver.touch_cached_file("pyassert-0.1.2.tar.gz")
        liveserver.touch_cached_file("yadt-2.0.0.tar.gz")

        index_page = download(liveserver.url + "simple/")

        assert_that(index_page).contains("pyassert").contains("yadt")

@test
def integration_test_with_hosted_and_cached_file():
    with LiveServer() as liveserver:
        liveserver.touch_cached_file("pyfix-0.1.2.tar.gz")
        liveserver.touch_cached_file("pyassert-0.1.2.tar.gz")
        liveserver.touch_hosted_file("committer-0.0.60.tar.gz")

        index_page = download(liveserver.url + "simple/")

        assert_that(index_page).contains("committer").contains("pyfix").contains("pyassert")

if __name__=='__main__':
    run_tests()
