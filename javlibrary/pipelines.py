# -*- coding: utf-8 -*-
import scrapy
from db import db
from db.artist import Artist
from db.topartist import TopArtist
from db.film import Film
from db.cast import Cast
from db.magnet import Magnet

class JavlibraryPipeline(object):
    def process_item(self, item, spider):
        return item

class ArtistPipeline(object):
    fid = 0
    aid = 1
    def open_spider(self, spider):
        self.session = db.getsession()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        if spider.name == 'Artist':
            a = Artist()
            self.aid += 1
            a.aid = self.aid
            a.artist_name = item['name']
            a.stag = item['stag']
            a.url = item['url']
            if self.session.query(Artist).filter(Artist.stag == a.stag).one_or_none() == None:
                self.session.add(film)
        elif spider.name == 'TopArtist':
            query =  self.session.query(Artist)
            a = query.filter(Artist.stag == item['stag']).all()[0]
            top = TopArtist()
            top.aid = a.aid
            top.artist_name = item['name']
            top.stag = item['stag']
            top.url = item['url']
            top.img = item['img']
            top.rank = item['rank']
            self.session.add(top)
        elif spider.name == 'Film':
            film = Film()
            self.fid += 1
            film.fid= self.fid
            film.file_name = item['name']
            film.tag = item['id']
            film.cover = item['cover']
            film.url = item['url']
            film.length = item['length']
            film.date = item['date']
            film.director = item['director']
            film.maker = item['maker']
            film.producer = item['producer']
            film.score = item['score']
            if self.session.query(Film).filter(Film.tag == film.tag).one_or_none() == None:
                self.session.add(film)
                for url in item['cast']:
                    a = self.session.query(Artist.aid).filter(Artist.url == url).first()
                    if a != None:
                        c = Cast()
                        c.aid = a.aid
                        c.fid = film.fid
                        self.session.add(c)
        elif spider.name == 'Magnet':
            magnet = Magnet()
            magnet.magnet_uri = item['magnet']
            magnet.fid = self.session.query(Film.fid).filter(Film.tag == item['tag']).first().fid
            self.session.add(magnet)
        self.session.flush()
        self.session.commit()
