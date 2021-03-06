import multiprocessing
import os
import pypiproxy.webapp
import shutil
import time
import urllib2

CONFIGURATION_FILE = "src/integrationtest/resources/pypiproxy_integrationtest.cfg"
MAX_WAITING_SECONDS = 10
TIMEOUT_SECONDS = 0.05


class LiveServer(object):
    def __init__(self):
        self.configuration = pypiproxy.configuration.Configuration(CONFIGURATION_FILE)

        _remove_directory_if_exists(self.configuration.hosted_packages_directory)
        _remove_directory_if_exists(self.configuration.cached_packages_directory)

        pypiproxy.services.initialize_services(self.configuration.hosted_packages_directory,
                                               self.configuration.cached_packages_directory,
                                               self.configuration.pypi_url)

        pypiproxy.initialize_logging(self.configuration.log_file)

        self.application = pypiproxy.webapp.application
        self.host = "127.0.0.1"
        self.port = 5000
        self.protocol = "http"

        self.url = "%s://%s:%s/" % (self.protocol, self.host, self.port)

    def __enter__(self):
        self.start_server_process()
        _wait_for(self.is_server_reachable)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.stop_server_process()

    def create_cached_file(self, *path_elements):
        self._create_file_with_content(self._join(self.configuration.cached_packages_directory, *path_elements),
                                       "cached content")

    def create_hosted_file(self, *path_elements):
        self._create_file_with_content(self._join(self.configuration.hosted_packages_directory, *path_elements),
                                       "hosted content")

    def is_server_reachable(self):
        try:
            urllib2.urlopen(self.url, timeout=TIMEOUT_SECONDS).close()
            return True
        except:
            return False

    def start_server_process(self):
        worker = lambda app, port: app.run(port=port)
        self._process = multiprocessing.Process(target=worker, args=(self.application, self.port))
        self._process.start()

    def stop_server_process(self):
        self._process.terminate()

    def _create_file_with_content(self, file_name, content):
        f = open(file_name, "w")
        try:
            f.write(content)
        finally:
            f.close()

    def _join(self, base_path, *path_elements):
        path_elements = [base_path] + list(path_elements)
        return os.path.join(*path_elements)



def _remove_directory_if_exists(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

def _wait_for(expression_to_be_true, max_waiting_seconds=MAX_WAITING_SECONDS, interval_seconds=TIMEOUT_SECONDS):
    waited_seconds = 0
    succeeded = False
    while (not succeeded) and (waited_seconds < max_waiting_seconds):
        succeeded = expression_to_be_true()
        time.sleep(interval_seconds)
        waited_seconds += interval_seconds

    return succeeded

