from integrationtestsupport import download
from liveserver import LiveServer
from pyassert import assert_that
from pyfix import test, run_tests

@test
def integration_test():
    with LiveServer() as liveserver:
        liveserver.touch_hosted_file("pyassert-0.1.2.tar.gz")
        liveserver.touch_hosted_file("pyassert-1.2.3.tar.gz")
        liveserver.touch_hosted_file("pyassert-2.3.4.tar.gz")

        index_page = download(liveserver.url + "simple/pyassert/")

        assert_that(index_page).starts_with("<!doctype html>\n<html>") \
                            .contains("<h1>Links for pyassert</h1>") \
                            .contains("<a href=\"/package/pyassert/2.3.4/pyassert-2.3.4.tar.gz\">pyassert-2.3.4.tar.gz</a><br/>") \
                            .contains("<a href=\"/package/pyassert/0.1.2/pyassert-0.1.2.tar.gz\">pyassert-0.1.2.tar.gz</a><br/>") \
                            .contains("<a href=\"/package/pyassert/1.2.3/pyassert-1.2.3.tar.gz\">pyassert-1.2.3.tar.gz</a><br/>") \
                            .ends_with("</html>")

if __name__ == '__main__':
    run_tests()
