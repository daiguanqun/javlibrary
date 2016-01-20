import db

class Magnet(object):
    pass

magnetTable = db.Table(
    "magnet", db.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('fid', db.Integer),
    db.Column('magnet_uri', db.VARCHAR(100)),
)

db.mapper(Magnet, magnetTable)
