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
        return _post_multipart(server.host, server.port, "/", raw_params, self._file_name, self._file_content)


def _create_form_part(boundary, form_fields):
    result = []
    for key, value in form_fields.iteritems():
        result.append('--' + boundary)
        result.append('Content-Disposition: form-data; name="%s"' % key)
        result.append('')
        result.append(value)
    return result


def _create_file_part(boundary, file_name, file_content):
    result = []
    result.append('--' + boundary)
    result.append('Content-Disposition: form-data; name="content"; filename="%s"' % file_name)
    result.append('Content-Type: application/x-tar')
    result.append('')
    result.append(file_content)
    return result

def _post_multipart(host, port, uri, form_fields, file_name, file_content):
    boundary = '----------bound@ry_$'
    content_type = 'multipart/form-data; boundary=%s' % boundary
    body_lines = []

    body_lines.extend(_create_form_part(boundary, form_fields))
    body_lines.extend(_create_file_part(boundary, file_name, file_content))

    body_lines.append('--' + boundary + '--')
    body_lines.append('')

    body = '\r\n'.join(body_lines)

    http_connection = httplib.HTTPConnection(host=host, port=port)
    http_connection.request('POST', uri, body, headers={'Content-Type': content_type})
    return http_connection.getresponse().status
