#!/usr/bin/env python

import sys

sys.path.append('src/main/python')

from pypiproxy.webapp import application
from pypiproxy import initialize

initialize("./pypiproxy.cfg")
application.run(debug=True)
