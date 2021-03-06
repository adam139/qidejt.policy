# -*- coding: UTF-8 -*-
from hashlib import sha1 as sha
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.textfield.value import RichTextValue
from plone.keyring.interfaces import IKeyManager
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from qidejt.policy.setuphandlers import _create_content
from qidejt.policy.setuphandlers import STRUCTURE
from qidejt.policy.testing import FunctionalTesting
from zope.component import getUtility

import hmac
import json
import unittest


def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')


class TestView(unittest.TestCase):

    layer = FunctionalTesting

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        for item in STRUCTURE:
            _create_content(item, portal)

    def test_sort_on(self):
        # check collection sort_on,sort_reversed etc.

        portal = self.layer['portal']
        item = portal['sqls']['qidexinwen']
        self.assertTrue(item.sort_on == "created")
        self.assertTrue(item.sort_reversed == True)
