#!/usr/bin/env python

import sys

sys.path.append("src/main/python")

from pypiproxy.webapp import application

application.run(debug=True)
