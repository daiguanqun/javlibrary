import db

class Artist(object):
    pass

artistTable = db.Table(
    "artist", db.metadata,
    db.Column('aid', db.Integer, primary_key=True),
    db.Column('artist_name', db.VARCHAR(50), nullable=False),
    db.Column('stag', db.VARCHAR(40), nullable=True),
    db.Column('url', db.VARCHAR(100), nullable=True),
)

db.mapper(Artist, artistTable)
