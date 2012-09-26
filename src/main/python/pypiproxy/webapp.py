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

import StringIO

from flask import Flask, request, render_template, abort

from .services import list_available_package_names, list_versions, get_package_content, upload_package

application = Flask(__name__)


@application.route("/package/<package_name>/<version>/<file_name>")
def handle_package_content(package_name, version, file_name):
    return get_package_content(package_name, version)


@application.route("/simple/<package_name>")
@application.route("/simple/<package_name>/")
def handle_version_list(package_name):
    version_list = [v for v in list_versions(package_name)]
    
    if not len(version_list):
        return "", 404
    
    return render_template("version-list.html", 
                           package_name=package_name,
                           versions_list=version_list)


@application.route("/simple")
def handle_package_list():
    return render_template("package-list.html",
                           package_name_list=list_available_package_names())


@application.route("/", methods=["POST"])
def handle_upload_package ():
    # TODO: What about authentication
    action = request.form[":action"]
    name = request.form["name"]
    version = request.form["version"]

    if action != "file_upload":
        print "Invalid action '{0}'".format(action)
        abort(400)

    if not name or not version:
        print "Missing name or version"
        abort(400)

    # TODO: Validate content type

    content = request.files["content"]
    buffer = StringIO.StringIO()
    content.save(buffer)

    upload_package(name, version, buffer.getvalue())
    return ""
