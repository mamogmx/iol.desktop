from Products.Five.browser import BrowserView
import simplejson as json
from iol.desktop.datatables import pgDataTables
from Acquisition import aq_parent
import sqlalchemy as sql
from plone import api
import datetime
import DateTime
from dateutil.parser import *


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%d/%m/%Y')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%d/%m/%Y')
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        elif isinstance(obj,DateTime.DateTime):
            return DateTime.DateTime.strftime('%d/%m/%Y')
        else:
            return super(DateTimeEncoder, self).default(obj)
            
def transformDate(obj):
    res = dict()
    for k,v in obj.iteritems():
        try:
            d = parse(v,ignoretz=True).strftime('%d/%m/%Y')
            obj[k] = d
        except:
            obj[k] = v  
    return obj   
        
class pgsearch(BrowserView):
    def __init__(self, context, request):
        # Each view instance receives context and request as construction parameters
        self.context = context
        self.request = request

    def search(self):
        request = self.request
        
        desktop = self.aq_parent

        desktop_manager = desktop.manager_groups or []
        desktop_reviewer = desktop.reviewer_groups  or []
        desktop_owner = desktop.owner_groups or []
        
        result = {'aaData': list(), 'sEcho': request.get('sEcho',0), 'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'error':''}
        if api.user.is_anonymous():
            result['message'] = 'Anonymous User'
            return result
        current = api.user.get_current()
        roles = api.user.get_roles(username=current.id)
        groups = [grp.id for grp in api.group.get_groups(username=current.id)]
        
        condition = None
        prms = json.loads(request.get('query','{}'))
        if 'Manager' in roles:
            condition = 1
        else:
            for grp in desktop_manager:
                if grp in groups:
                    prms['iol_manager']=dict(
                        op='intersect',
                        name='iol_manager',
                        subname='',
                        value= groups + [current.id],
                        type='text'
                    )
                    condition = 1
            if not condition:
                for grp in desktop_reviewer:
                    if grp in groups:
                        prms['iol_reviewer']=dict(
                            op='intersect',
                            name='iol_reviewer',
                            subname='',
                            value= groups + [current.id],
                            type='text'
                        )
                        condition = 1
                if not condition:
                    for grp in desktop_owner:
                        if grp in groups:
                            prms['iol_owner']=dict(
                                op='intersect',
                                name='iol_owner',
                                subname='',
                                value= groups + [current.id],
                                type='text'
                            )
                            condition = 1

        if not condition:
            result['message'] = 'User not in groups'
            return result
        request.set('query',prms)
        engine = sql.create_engine(desktop.conn_string)
        connection = engine.connect()
        tb = desktop.db_table
        sk = desktop.db_schema
        dt = pgDataTables(sk,tb,request)

        queryTot = dt.findTotal()
        query = dt.findResult()
        resTot = connection.execute(sql.text(queryTot))
        totali = int(resTot.fetchall()[0]["totali"])
        result["iTotalRecords"] = totali

        res = connection.execute(sql.text(query))
        d = res.fetchall()
        for r in d:
            try:
                r = dict(r)
                data = json.loads(json.dumps(r['data']),object_hook = transformDate)
            except Exception as e:
                print str(e)
                data=dict()
            data['id'] = r['id']
            data['review_state'] = r['review_state']
            data['plominodb'] = r['plominodb']
            data['object_url'] = r['url']
            data['object_path'] = r['path']
            result['aaData'].append(data)
        result['query'] = query
        result['iTotalDisplayRecords'] = totali

        return result

    def __call__(self):
        res = self.search()
        self.request.RESPONSE.headers['Content-Type'] = 'application/json'
        return json.dumps(res)