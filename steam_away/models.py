from steam_away import db
from datetime import datetime

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean)
    name = db.Column(db.String)
    visits = db.Column(db.Integer)
    oauth_id = db.Column(db.String)

    def __init__(self, name, oauth_id, admin=False):
        self.admin = admin
        self.name = name
        self.oauth_id = oauth_id
        self.visits = 0

    def __repr__(self):
        if self.admin:
            return "<%s (Admin)>" % self.name
        return '<%s>' % self.name

class Giveaway(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    active = db.Column(db.Boolean)
    done = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.active = False
        self.done = False

    def __repr__(self):
        return "<GA: %s>" % self.name

class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    key = db.Column(db.String)

    giveaway_id = db.Column(db.Integer, db.ForeignKey('giveaway.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    giveaway = db.relationship('Giveaway', backref=db.backref('keys', lazy='dynamic'),)
    owner = db.relationship('Person', backref=db.backref('loot', lazy='select'))

    def __init__(self, name, key):
        self.name = name
        self.key = key

    def __repr__(self):
        return "<K: %s, %s>" % (self.name, self.id)
