from pyassert import assert_that
from pyfix import after, before, given, test, run_tests
from liveserver import LiveServer
from staticpypi import StaticPyPiServer
from integrationtestsupport import download

@test
def integration_test():
    with StaticPyPiServer(), LiveServer() as liveserver:
        index_page = download(liveserver.url + "simple/")

        assert_that(index_page).contains("public-a").contains("public-b").contains("public-c")


if __name__=='__main__':
    run_tests()
