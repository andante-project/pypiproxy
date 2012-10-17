import multiprocessing
import staticpypiapplication

application = staticpypiapplication.application
host = "127.0.0.1"
port = 5001
protocol = "http"

class StaticPyPiServer (object):
    def __init__(self):
        self._process = None

    def __enter__(self):
        worker = lambda application, port: application.run(port=port)
        self._process = multiprocessing.Process(target=worker, args=(application, port))
        self._process.start()
        return self._process

    def __exit__(self, exception_type, exception_value, traceback):
        self._process.terminate()
