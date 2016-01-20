import db

class Film(object):
    pass

filmTable = db.Table(
    "film", db.metadata,
    db.Column('fid', db.Integer, primary_key=True),
    db.Column('tag', db.VARCHAR(40), nullable=False),
    db.Column('file_name', db.VARCHAR(1000), nullable=False),
    db.Column('cover', db.VARCHAR(1000), nullable=True),
    db.Column('url', db.VARCHAR(200), nullable=True),
    db.Column('length', db.Integer, nullable=True),
    db.Column('date', db.VARCHAR(100), nullable=True),
    db.Column('director', db.VARCHAR(100), nullable=True),
    db.Column('maker', db.VARCHAR(100), nullable=True),
    db.Column('producer', db.VARCHAR(100), nullable=True),
    db.Column('score', db.FLOAT, nullable=True),
    db.Column('magnet', db.VARCHAR(1000), nullable=True),
)

db.mapper(Film, filmTable)
