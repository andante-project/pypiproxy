pypiproxy [![Build Status](https://secure.travis-ci.org/yadt/pypiproxy.png)](http://travis-ci.org/yadt/pypiproxy)
=========

This PyPI implementation has been created with *continuous delivery* in mind.  
*pypiproxy* will cache the requested artifacts and will deliver them if the public cheeseshop is not reachable. 

## Uploading a .tar.gz

```bash
python setup.py sdist upload -r http://pypiproxy.domain:1234/
```

## Installing a .tar.gz using pip

```bash
pip install flask --index http://pypiproxy.domain:1234/simple
```