from __init__ import db
from models import User



u = User(username='mainuser',password='password', port='9002', token=-1)
db.session.add(u)

u2 = User(username='jmoore',password='fun', port='9003', token=-1)
db.session.add(u2)

u3 = User(username='xstream',password='third', port='9004', token=-1)
db.session.add(u3)

db.session.commit()
