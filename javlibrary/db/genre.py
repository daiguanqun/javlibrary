import db

class Genre(object):
    pass

genreTable = db.Table(
    "genre", db.metadata,
    db.Column('gid', db.Integer, primary_key=True),
    db.Column('genre_name', db.VARCHAR(50), nullable=False),
    db.Column('url', db.VARCHAR(100), nullable=True),
)

db.mapper(Genre, genreTable)
