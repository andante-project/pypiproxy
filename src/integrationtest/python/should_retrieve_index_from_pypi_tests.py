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


if __name__=='__main__':
    run_tests()
