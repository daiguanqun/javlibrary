import db

class Cast(object):
    pass

castTable = db.Table(
    "cast", db.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('aid', db.Integer),
    db.Column('fid', db.Integer),
)

db.mapper(Cast, castTable)
