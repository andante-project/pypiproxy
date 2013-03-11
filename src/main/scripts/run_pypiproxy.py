#!/usr/bin/env python

import sys

from pypiproxy.webapp import application
from pypiproxy import initialize

initialize("pypiproxy.cfg")
application.run(debug=True)
