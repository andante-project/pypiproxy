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
        multi_part_request = MultiPartRequestBuilder() \
                                .form_field(":action", "file_upload") \
                                .form_field("name", self._package_name) \
                                .form_field("version", self._package_version) \
                                .file(self._file_name, self._file_content).build()

        return send_post_request(server.host, server.port, "/", multi_part_request)


class MultiPartRequest(object):
    def __init__(self, body, headers):
        self._body = body
        self._headers = headers

    @property
    def body(self):
        return self._body

    @property
    def headers(self):
        return self._headers


class MultiPartRequestBuilder (object):
    def __init__(self):
        self.body_buffer = StringIO()
        self.boundary = "---------abcdefghijklmnop$"
        self.file_content = "default content"
        self.file_name = "default.txt"
        self.form_fields = {}

    def form_field(self, key, value):
        self.form_fields[key] = value
        return self

    def file(self, file_name, file_content):
        self.file_name = file_name
        self.file_content = file_content
        return self

    def build(self):
        self._write_form_fields()
        self._write_file()
        self._write_line("--{0}--".format(self.boundary))
        self._write_line()

        body = self.body_buffer.getvalue()
        headers = {"Content-Type": "multipart/form-data; boundary={0}".format(self.boundary)}
        return MultiPartRequest(body, headers)

    def _write_file(self):
        self._write_line("--" + self.boundary)
        self._write_line("Content-Disposition: form-data; name=\"content\"; filename=\"{0}\"".format(self.file_name))
        self._write_line("Content-Type: application/x-tar")
        self._write_line()
        self._write_line(self.file_content)

    def _write_form_fields(self):
        for key, value in self.form_fields.iteritems():
            self._write_line("--{0}".format(self.boundary))
            self._write_line("Content-Disposition: form-data; name=\"{0}\"".format(key))
            self._write_line()
            self._write_line(value)

    def _write_line(self, text=""):
        self.body_buffer.writelines("{0}\n".format(text))


def send_post_request(host, port, url, multi_part_request):
    http_connection = httplib.HTTPConnection(host=host, port=port)
    http_connection.request(method="POST", url=url, body=multi_part_request.body, headers=multi_part_request.headers)
    return http_connection.getresponse().status
