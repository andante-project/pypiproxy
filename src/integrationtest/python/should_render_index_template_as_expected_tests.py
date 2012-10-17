from integrationtestsupport import download
from liveserver import LiveServer
from pyassert import assert_that
from pyfix import test, run_tests
from staticpypi import StaticPyPiServer

@test
def integration_test():
    with StaticPyPiServer():
        with LiveServer() as liveserver:
            liveserver.touch_hosted_file("yadt-1.2.3.tar.gz")

            index_page = download(liveserver.url + "simple/")

            assert_that(index_page).starts_with("<!doctype html>\n<html>") \
                            .contains("<h1>List of Packages</h1>") \
                            .contains("<a href=\"/simple/public-a\">public-a</a><br/>") \
                            .contains("<a href=\"/simple/public-b\">public-b</a><br/>") \
                            .contains("<a href=\"/simple/public-c\">public-c</a><br/>") \
                            .contains("<a href=\"/simple/yadt\">yadt</a><br/>") \
                            .ends_with("</html>")

if __name__ == '__main__':
    run_tests()
