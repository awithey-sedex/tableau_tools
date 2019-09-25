#!/bin/python3
# coding=utf-8

import xml.etree.ElementTree as etree

from tableau_tools.tableau_rest_api import TableauRestApiConnection30, TableauRestApiConnection31, TableauRestApiConnection32, TableauRestApiConnection33
from tableau_tools.tableau_rest_api.permissions import ProjectPermissions28, DatasourcePermissions28, \
    WorkbookPermissions28
from requests.exceptions import HTTPError
try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO

# Turn off SSL warnings in requests library
import urllib3
urllib3.disable_warnings()
