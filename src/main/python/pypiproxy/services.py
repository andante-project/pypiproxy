__author__ = "Michael Gruber"

from .packageindex import PackageIndex

_hosted_packages_index = PackageIndex("hosted", "packages/hosted")

def list_available_package_names():
    """
        @return: iterable of strings
    """
    return _hosted_packages_index.list_available_package_names()


def list_versions(name):
    """
        @return: iterable of strings
    """
    return _hosted_packages_index.list_versions(name)


def get_package_content(name, version):
    """
        @return: a file-like object
    """
    return _hosted_packages_index.get_package_content(name, version)


def upload_package(name, version, content_stream):
    _hosted_packages_index.add_package(name, version, content_stream)
