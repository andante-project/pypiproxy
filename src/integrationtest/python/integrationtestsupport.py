import httplib
import urllib2

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
        raw_params = {':action': 'file_upload',
                      'name': self._package_name,
                      'version': self._package_version}
        return MultiPartRequestBuilder().form_data(raw_params).file(self._file_name, self._file_content).send_post_request(server.host, server.port, "/")


class MultiPartRequestBuilder (object):
    def __init__(self):
        self.boundary = '---------abcdefghijklmnop$'
        self.body_lines = []

    def form_data(self, form_fields):
        for key, value in form_fields.iteritems():
            self.body_lines.append('--' + self.boundary)
            self.body_lines.append('Content-Disposition: form-data; name="%s"' % key)
            self.body_lines.append('')
            self.body_lines.append(value)
        return self

    def file(self, file_name, file_content):
        self.body_lines.append('--' + self.boundary)
        self.body_lines.append('Content-Disposition: form-data; name="content"; filename="%s"' % file_name)
        self.body_lines.append('Content-Type: application/x-tar')
        self.body_lines.append('')
        self.body_lines.append(file_content)
        return self

    def send_post_request(self, host, port, uri):
        content_type = 'multipart/form-data; boundary=%s' % self.boundary

        self.body_lines.append('--' + self.boundary + '--')
        self.body_lines.append('')

        body = '\n'.join(self.body_lines)

        http_connection = httplib.HTTPConnection(host=host, port=port)
        http_connection.request('POST', uri, body, headers={'Content-Type': content_type})
        return http_connection.getresponse().status
