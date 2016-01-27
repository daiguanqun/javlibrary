import db

class Category(object):
    pass

categoryTable = db.Table(
    "category", db.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('fid', db.Integer),
    db.Column('gid', db.Integer),
)

db.mapper(Category, categoryTable)
