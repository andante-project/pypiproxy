from flask import Flask

application = Flask(__name__)

@application.route("/simple/yadt/")
def handle_yadt_versions():
    return """<!doctype html><html><head></head><body>
<a href="yadt-0.1.2.tar.gz">yadt-0.1.2</a><br/>
<a href="yadt-1.2.3.tar.gz">yadt-1.2.3</a><br/>
<a href="yadt-2.3.4.tar.gz">yadt-2.3.4</a><br/>
</body></html>"""


@application.route("/simple/")
def handle_index():
    return """<!doctype html><html><head></head><body>
<a href="/simple/public-a/">public-a</a><br/>
<a href="/simple/public-b/">public-b</a><br/>
<a href="/simple/public-c/">public-c</a><br/>
</body></html>"""
