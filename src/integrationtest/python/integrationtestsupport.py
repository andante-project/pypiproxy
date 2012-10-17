import httplib
import urllib2

from StringIO import StringIO
from werkzeug.datastructures import ImmutableList


def download(url):
    return urllib2.urlopen(url, timeout=2).read()


def upload():
    return UploadBuilder()


class UploadBuilder:
    def __init__ (self):
        self._file_name = "filename.txt"
        self._file_content = "file content"
        self._package_name = "package_name"
        self._package_version = "0.1.2"

    def file(self, file_name):
        self.file_name = file_name
        return self

    def file_content(self, content):
        self._file_content = content
        return self

    def package_name(self, name):
        self._package_name = name
        return self

    def package_version(self, version):
        self._package_version = version
        return self

    def to(self, server):
        form_fields = {":action": "file_upload",
                      "name": self._package_name,
                      "version": self._package_version}
        multi_part_request = MultiPartRequestBuilder().form_data(form_fields).file(self._file_name, self._file_content).build()
        return send_post_request(server.host, server.port, "/", multi_part_request)

class MultiPartRequest(object):
    def __init__(self, body, headers):
        self.body = body
        self.headers = headers

class MultiPartRequestBuilder (object):
    def __init__(self):
        self.boundary = "---------abcdefghijklmnop$"
        self.body_buffer = StringIO()

    def _write_line(self, text=""):
        self.body_buffer.writelines("{0}\n".format(text))

    def form_data(self, form_fields):
        for key, value in form_fields.iteritems():
            self._write_line("--{0}".format(self.boundary))
            self._write_line("Content-Disposition: form-data; name=\"{0}\"".format(key))
            self._write_line()
            self._write_line(value)
        return self

    def file(self, file_name, file_content):
        self._write_line("--" + self.boundary)
        self._write_line("Content-Disposition: form-data; name=\"content\"; filename=\"{0}\"".format(file_name))
        self._write_line("Content-Type: application/x-tar")
        self._write_line()
        self._write_line(file_content)
        return self

    def build(self):
        self._write_line("--{0}--".format(self.boundary))
        self._write_line()

        body = self.body_buffer.getvalue()
        headers = {"Content-Type": "multipart/form-data; boundary={0}".format(self.boundary)}
        return MultiPartRequest(body, headers)

def send_post_request(host, port, url, multi_part_request):
    http_connection = httplib.HTTPConnection(host=host, port=port)
    http_connection.request(method="POST", url=url, body=multi_part_request.body, headers=multi_part_request.headers)
    return http_connection.getresponse().status
