#-*- coding: UTF-8 -*-
from hashlib import sha1 as sha
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.textfield.value import RichTextValue
from plone.keyring.interfaces import IKeyManager
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from plone.namedfile.file import NamedImage
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from qidejt.policy.setuphandlers import _create_content
from qidejt.policy.setuphandlers import import_article
from qidejt.policy.setuphandlers import STRUCTURE
from qidejt.policy.testing import FunctionalTesting
from zope.component import getUtility

import hmac
import json
import os
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
        
        import_article(portal)
        self.portal = portal
    
    def test_front(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))       

        import transaction
        transaction.commit()
        import pdb
        pdb.set_trace()
        obj = portal.absolute_url() + '/@@index.html'    
        browser.open(obj)
 
        outstr = u"图片新闻3"
        self.assertTrue(outstr in browser.contents)
        
    def test_folder_ajax_view(self):        
        request = self.layer['request']       
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'formstart': 0,
                        'size':10                                                                   
                        }
# Look up and invoke the view via traversal
        target = self.portal['qidedongtai']
        view = target.restrictedTraverse('@@favoritemore')
        result = view()
        outstr = u'class="col-md-9 title"'

        self.assertTrue(outstr in json.loads(result)['outhtml'])
      
        
    def test_folder_view(self):        

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))       

        import transaction
        transaction.commit()
        target = self.portal['qidedongtai']
        page = target.absolute_url() + '/@@tableview'    
        browser.open(page)
 
        outstr = 'id="tablecontent"'
        self.assertTrue(outstr in browser.contents)      
