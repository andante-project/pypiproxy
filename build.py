#   pypiproxy
#   Copyright 2012-2013 Michael Gruber, Alexander Metzner, Maximilien Riehl
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

"""
    A proxy server for the python package index.
"""

__author__ = 'Michael Gruber, Alexander Metzner, Maximilien Riehl'

from pybuilder.core import init, use_plugin, Author

use_plugin("filter_resources")

use_plugin("python.core")
use_plugin("python.pyfix_unittest")
use_plugin("python.integrationtest")
use_plugin("python.coverage")
use_plugin("python.pydev")
use_plugin("python.distutils")
use_plugin('copy_resources')

use_plugin("python.install_dependencies")

default_task = ["analyze", "publish"]

name = "pypiproxy"
version = "0.3.1"
summary = "A proxy server for the python package index."
authors = (Author("Alexander Metzner", "halimath.wilanthaou@gmail.com"),
           Author("Michael Gruber", "aelgru@gmail.com"),
           Author("Maximilien Riehl", "maximilien.riehl@gmail.com"))
url = "https://github.com/aelgru/pypiproxy"
license = "Apache License, Version 2.0"


@init
def initialize(project):
    project.build_depends_on("mockito")
    project.build_depends_on("pyassert")

    project.depends_on("flask")

    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property("filter_resources_glob").append("**/pypiproxy/__init__.py")
    project.get_property('copy_resources_glob').append('setup.cfg')
    project.include_file("pypiproxy", "templates/*.html")

    project.set_property("coverage_threshold_warn", 85)
    project.set_property("coverage_break_build", False)

@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os

    project.version = '%s-%s' % (project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['install_dependencies', 'package']
    project.set_property('install_dependencies_use_mirrors', False)
    project.get_property('distutils_commands').append('bdist_rpm')
