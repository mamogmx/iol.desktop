

def greaterthen(key,v):
    return "(coalesce(%s,'')<>'' AND (%s)::%s > '%s'::%s)" %(key,key,v["type"],v["value"][0],v["type"])
def lesserthen(key,v):
    return "(coalesce(%s,'')<>'' AND (%s)::%s < '%s'::%s)" %(key,key,v["type"],v["value"][0],v["type"])
def inlist(key,v):
    return "((%s) IN ('%s'))" %(key,"','".join(v['value']))
def between(key,v):
    return "(coalesce(%s,'')<>'' AND ((%s)::%s < '%s'::%s) AND ((%s)::%s > '%s'::%s)" %(key,key,v['type'],v['value'][0],key,v['type'],v['value'][1])
def contains(key,v):
    return "((%s) ILIKE '%%s%')" %(key,v['value'][0])
def equal(key,v):
    return "(coalesce(%s,'')<>'' AND (%s)::%s = '%s'::%s)" %(key,key,v["type"],v["value"][0],v["type"])

options = {
    'gt' : greaterthen,
    'lt' : lesserthen,
    'in' : inlist,
    'btw' : between,
    'contains' : contains,
    'eq' : equal,
}

class pgDataTables(object):
    def __init__(self,sk,tb,req):
        self.schema = sk
        self.table = tb
        self.request = req
        self.queryParams = req.get('query',dict())
        self.lim = req.get('iDisplayLength','-1')
        self.offset = req.get('iDisplayStart','0')

    def filter(self, mode = 'AND'):
        if not self.queryParams:
            return 'true'
        flt = list()
        for key,v in self.queryParams.keys():
            flt.append(options[v['op']](key,v))
        return (' %s ' %mode).join(flt)

    def limit(self):
        sLimit = "LIMIT %s" %self.lim
        return "%s OFFSET %s" %(sLimit,self.offset)
    def order(self):
        return ""
    def findResult(self):
        sFilter = self.filter()
        sLimit = self.limit()
        sOrder = self.order()
        query = "SELECT * FROM %s.%s WHERE %s %s %s" %(self.schema,self.table,sFilter,sLimit,sOrder)
        return query

    def findTotal(self):

        sFilter = self.filter()
        query = "SELECT count(*) as totali FROM %s.%s WHERE %s" %(self.schema,self.table,sFilter)
        return query

