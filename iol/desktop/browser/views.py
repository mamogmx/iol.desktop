from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from plone.dexterity.browser.view import DefaultView

import simplejson as json

class pgsearch(BrowserView):
    def __call__(self):
        return json.dumps(dict(a))