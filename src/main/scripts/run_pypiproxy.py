#!/usr/bin/env python

import socket
from pypiproxy.webapp import application
from pypiproxy import initialize

initialize("/etc/pypiproxy/pypiproxy.cfg")
application.run(host=socket.getfqdn())
