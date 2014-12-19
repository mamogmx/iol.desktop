import zope.interface
from z3c.form.validator import SimpleFieldValidator
from sqlalchemy import create_engine

class validateConn(SimpleFieldValidator):
    def validate(self,value):
        try:
            engine = create_engine(value)
        except:
            msg = u"Invalid connection string"
            raise zope.interface.Invalid(msg)