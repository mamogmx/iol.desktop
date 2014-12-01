from plone import api
import logging


default_profile = 'profile-iol.desktop:default'

logger = logging.getLogger('iol.desktop')

def update_groups(setup):
    setup.runImportStepFromProfile(default_profile, 'groups')
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type='pg_desktop')
    for brain in brains:
        desk = brain.getObject()
        if isinstance(desk.owner_groups,basestring):
            owner = desk.owner_groups.split(',') or []
            desk.owner_groups = owner
        if isinstance(desk.reviewer_groups,basestring):
            reviewer = desk.reviewer_groups.split(',') or []
            desk.reviewer_groups_groups = reviewer
        if isinstance(desk.manager_groups,basestring):
            manager = desk.manager_groups.split(',') or []
            desk.manager_groups = manager
