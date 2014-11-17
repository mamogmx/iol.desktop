from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from plone.dexterity.browser.view import DefaultView

import simplejson as json

class pgsearch(BrowserView):
    def __call__(self):
        self.REQUEST.RESPONSE.headers['Content-Type'] = 'application/json'
        return json.dumps(dict(a=1))