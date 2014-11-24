from Products.Five.browser import BrowserView
import simplejson as json
from iol.desktop.datatables import pgDataTables
from Acquisition import aq_parent
import sqlalchemy as sql
from plone import api


class pgsearch(BrowserView):
    def __init__(self, context, request):
        # Each view instance receives context and request as construction parameters
        self.context = context
        self.request = request

    def search(self):
        request = self.request
        desktop = self.aq_parent
        desktop_mng = desktop.manager_groups or ''
        desktop_rvw = desktop.reviewer_groups or ''
        desktop_own = desktop.owner_groups or ''
        
        desktop_manager = desktop_mng.split(',') or []
        desktop_reviewer = desktop_rvw.split(',') or []
        desktop_owner = desktop_own.split(',') or []
        
        result = {'aaData': list(), 'sEcho': request.get('sEcho',0), 'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'error':''}
        if api.user.is_anonymous():
            return result
        current = api.user.get_current()
        roles = api.user.get_roles(username=current.id)
        groups = [grp.id for grp in api.group.get_groups(username=current.id)]
        
        condition = None
        prms = request.get('query',dict())
        if 'Manager' in roles:
            condit = 1
        else:
            for grp in desktop_manager:
                if grp in groups:
                    condition = 1
            if not condition:
                for grp in desktop_reviewer:
                    if grp in groups:
                        prms['istruttore']=dict(
                            op='eq',
                            name='data',
                            subname='istruttore',
                            value=[current.id],
                            type='text'
                        )
                        condition = 1
                if not condition:
                    for grp in desktop_reviewer:
                        if grp in groups:
                            prms['owner']=dict(
                                op='eq',
                                name='owner',
                                subname='',
                                value=[current.id],
                                type='text'
                            )
        request.set('query',prms)
        engine = sql.create_engine(desktop.conn_string)
        connection = engine.connect()
        tb = desktop.db_table
        sk = desktop.db_schema
        dt = pgDataTables(sk,tb,request)

        queryTot = dt.findTotal()
        query = dt.findResult()
        
        resTot = connection.execute(queryTot)
        totali = int(resTot.fetchall()[0]["totali"])
        result["iTotalRecords"] = totali

        res = connection.execute(query)
        d = res.fetchall()
        for r in d:
            try:
                r = dict(r)
                data = r['data']
            except Exception as e:
                print str(e)
                data=dict()
            data['id'] = r['id']
            result['aaData'].append(data)
        result['iTotalDisplayRecords'] = totali

        return result

    def __call__(self):
        res = self.search()
        self.request.RESPONSE.headers['Content-Type'] = 'application/json'
        return json.dumps(res)