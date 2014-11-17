from Products.Five.browser import BrowserView
import simplejson as json
from iol.desktop.datatables import pgDataTables
from Acquisition import aq_parent
import sqlalchemy as sql


class pgsearch(BrowserView):
    def __init__(self, context, request):
        # Each view instance receives context and request as construction parameters
        self.context = context
        self.request = request

    def search(self):
        request = self.request
        desktop = self.aq_parent
        result = {'aaData': list(), 'sEcho': request.get('sEcho',0), 'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'error':''}
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
        for r in res:
            data = json.loads(r)
            data[id] = r["id"]
            result['aaData'].append(data)
        result['iTotalDisplayRecords'] = len(result['aaData'])

        return result

    def __call__(self):
        res = self.search()
        request.RESPONSE.headers['Content-Type'] = 'application/json'
        return json.dumps(res))