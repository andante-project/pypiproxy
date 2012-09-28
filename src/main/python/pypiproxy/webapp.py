#   pypiproxy
#   Copyright 2012 Michael Gruber, Alexander Metzner
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

__author__ = "Michael Gruber, Alexander Metzner"

import logging
import StringIO

from flask import Flask, request, render_template, abort, make_response

from pypiproxy import __version__ as version
from .services import (list_available_package_names, list_versions, get_package_content, add_package,
                       get_package_statistics)


LOGGER = logging.getLogger("pypiproxy.webapp")

application = Flask(__name__)

def render_application_template(template_name, **template_parameters):
    template_parameters["version"] = version
    return render_template(template_name, **template_parameters)


@application.route("/")
def handle_index():
    LOGGER.debug("Handling request for index")

    number_of_packages, number_of_unique_packages = get_package_statistics()
    return render_application_template("index.html", **locals())


@application.route("/package/<package_name>/<version>/<file_name>")
def handle_package_content(package_name, version, file_name):
    LOGGER.debug("Handling request to download package %s", file_name)

    content = get_package_content(package_name, version)
    if content is None:
        abort(404)

    response = make_response(content)
    response.headers["Content-Disposition"] = "attachment; filename={0}".format(file_name)
    response.headers["Content-Type"] = "application/x-gzip"
    return response


@application.route("/simple/<package_name>")
@application.route("/simple/<package_name>/")
def handle_version_list(package_name):
    LOGGER.debug("Handling request to list versions for '%s'", package_name)

    version_list = [v for v in list_versions(package_name)]

    if not len(version_list):
        return "", 404

    return render_application_template("version-list.html",
        package_name=package_name,
        versions_list=version_list)


@application.route("/simple")
@application.route("/simple/")
def handle_package_list():
    LOGGER.debug("Handling request to list all packages")

    return render_application_template("package-list.html",
        package_name_list=list_available_package_names())


@application.route("/", methods=["POST"])
def handle_upload_package():
    LOGGER.debug("Handling request to upload package")

    # TODO: What about authentication
    action = request.form[":action"]
    name = request.form["name"]
    version = request.form["version"]

    if action != "file_upload":
        abort(400)

    # TODO: Validate content type

    content = request.files["content"]
    buffer = StringIO.StringIO()
    content.save(buffer)

    add_package(name, version, buffer.getvalue())
    return ""
