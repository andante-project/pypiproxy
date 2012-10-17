import multiprocessing
import staticpypiapplication

port = 5001

class StaticPyPiServer (object):
    def __init__(self):
        worker = lambda application, port: application.run(port=port)
        self._process = multiprocessing.Process(target=worker, args=(staticpypiapplication.application, port))

    def __enter__(self):
        self._process.start()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._process.terminate()
