from pythonbuilder.core import init, use_plugin, Author

use_plugin("filter_resources")

use_plugin("python.core")
use_plugin("python.pyfix_unittest")
use_plugin("python.integrationtest")
use_plugin("python.coverage")
use_plugin("python.pychecker")
use_plugin("python.pydev")
use_plugin("python.distutils")

use_plugin("python.install_dependencies")

default_task = ["analyze", "publish"]

version = "0.1.0"
summary = "A framework for writing automated software tests (non xUnit based)"
authors = (Author("Alexander Metzner", "halimath.wilanthaou@gmail.com"),
	   Author("Michael Gruber", "aelgru@gmail.com"))
url     = "https://github.com/aelgru/pypiproxy"
license = "Apache License, Version 2.0"

@init
def init (project):
    project.build_depends_on("coverage")
    project.build_depends_on("mockito")
    project.build_depends_on("pyassert")
    project.build_depends_on("pyfix")

    project.get_property("filter_resources_glob").append("**/pypiproxy/__init__.py")

    project.set_property("pychecker_break_build", True)
    
    project.set_property("coverage_threshold_warn", 85)
    project.set_property("coverage_break_build", False)

    project.get_property("distutils_commands").append("bdist_egg")
    project.set_property("distutils_classifiers", [
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'])

