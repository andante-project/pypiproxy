from flask import Flask

application = Flask(__name__)

@application.route("/simple/public-a/")
def handle_index():
    return """<!doctype html><html><head></head><body>
<a href="public-a-0.1.2.tar.gz">public-a-0.1.2</a><br/>
<a href="public-a-1.2.3.tar.gz">public-a-1.2.3</a><br/>
<a href="public-a-2.3.4.tar.gz">public-a-2.3.4</a><br/>
</body></html>"""


@application.route("/simple/")
def handle_index():
    return """<!doctype html><html><head></head><body>
<a href="/simple/public-a/">public-a</a><br/>
<a href="/simple/public-b/">public-b</a><br/>
<a href="/simple/public-c/">public-c</a><br/>
</body></html>"""
