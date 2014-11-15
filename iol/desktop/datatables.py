__author__ = 'mamo'

def gt(key,v):
    return "(coalesce(%s,'')<>'' AND (%s)::%s > '%s'::%s)" %(key,key,v["type"],v["value"][0],v["type"])
def lt(key,v):
    return "(coalesce(%s,'')<>'' AND (%s)::%s < '%s'::%s)" %(key,key,v["type"],v["value"][0],v["type"])
def inlist(key,v):
    return "((%s) IN ('%s'))" %(key,"','".join(v['value']))
def btw(key,v):
    return "(coalesce(%s,'')<>'' AND ((%s)::%s < '%s'::%s) AND ((%s)::%s > '%s'::%s)" %(key,key,v['type'],v['value'][0],key,v['type'],v['value'][1])
def contains(key,v):
    return "((%s) ILIKE '%%s%')" %(key,v['value'][0])
def eq(key,v):
    return "(coalesce(%s,'')<>'' AND (%s)::%s = '%s'::%s)" %(key,key,v["type"],v["value"][0],v["type"])

options = dict('gt' = gt, 'lt' = lt, 'in' = inlist, 'btw' = btw, 'contains' = contains, 'eq' = eq)

class pgDataTables(object):
    def __init__(self,sk,tb,req):
        self.schema = sk
        self.table = tb
        self.request = req

    def filter(self, mode = 'AND'):
        if not filter:
            return 'true'
        flt = list()
        for key,v in self.request['query'].keys():
            flt.append(options[v['op']](key,v))
        return (' %s ' %mode).join(flt)

    def limit(self,lim,offset):
        sLimit = ""
        if lim != "-1":
            sLimit = "LIMIT %s" %lim
        if offset:
            off = offset
        else:
            off = "0"
        return "%s OFFSET %s" %(sLimit,off)
    def order(self):
        return ""
    def findResult(self):
        sFilter = self.filter(params['query'])
        sLimit = self.limit(self.request['iDisplayLength'],self.request['iDisplayStart'])
        sOrder = self.order()
        query = "SELECT * FROM %s.%s WHERE %s %s %s" %(self.schema,self.table,sFilter,sLimit,sOrder)
        return query

    def findTotal(self):
        sFilter = self.filter(params['query'])
        query = "SELECT count(*) as totali FROM %s.%s WHERE %s" %(self.schema,self.table,sFilter)
        return query

