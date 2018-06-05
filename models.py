from flask_sqlalchemy import SQLAlchemy

# Instantiate a database object
db = SQLAlchemy()

class Block(db.Model):
    id = db.Column(db.Integer, unique = True, primary_key = True)
    number = db.Column(db.Integer)
    line = db.Column(db.String(25))
    length = db.Column(db.Float)
    grade = db.Column(db.Float)
    speedLimit = db.Column(db.Integer)
    elevation = db.Column(db.Float)
    cumulative_elevation = db.Column(db.Float)

    occupancy = db.Column(db.Boolean)

    switch_id = db.Column(db.Integer, db.ForeignKey('switch.id'))
    switch = db.relationship("Switch", backref=db.backref("block"))

    station_id = db.Column(db.Integer, db.ForeignKey('station.id'))
    station = db.relationship("Station", backref=db.backref("block"))

    crossing_id = db.Column(db.Integer, db.ForeignKey('crossing.id'))
    crossing = db.relationship("Crossing", backref=db.backref("block"))

    train_id = db.Column(db.Integer, db.ForeignKey('train.id'))

    message = db.Column(db.String(100))

    def _repr_(self):
        return "<Block {}>".format(repr(self.id))

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     text = db.Column(db.String(100))
#
#     def _repr_(self):
#         return "<Message {}>".format(repr(self.id))

class Station(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)

    def _repr_(self):
    	return "<Crossing {}>".format(repr(self.id))

class Switch(db.Model):
    id = db.Column(db.Integer, unique = True, primary_key = True)
    state = db.Column(db.Boolean)

    lights = db.relationship('Light', backref='switch', lazy='dynamic')

    def _repr_(self):
        return "<Switch {}>".format(repr(self.id))

class Crossing(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    state = db.Column(db.Boolean)
    lights = db.relationship('Light', backref='crossing', lazy='dynamic')

    def _repr_(self):
    	return "<Crossing {}>".format(repr(self.id))

class Light(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    state = db.Column(db.Boolean)
    switch_id = db.Column(db.Integer, db.ForeignKey('switch.id'))
    crossing_id = db.Column(db.Integer, db.ForeignKey('crossing.id'))

    def _repr_(self):
    	return "<Light {}>".format(repr(self.id))

class Train(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    length = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    mass = db.Column(db.Float)
    speed = db.Column(db.Float)
    crewCount = db.Column(db.Integer)
    passengerCount = db.Column(db.Integer)
    leftDoorState = db.Column(db.Boolean)
    rightDoorState = db.Column(db.Boolean)

    # blocks = db.relationship('Block', backref='train', lazy='dynamic')
    front_block_id = db.Column(db.Integer, db.ForeignKey('block.id'))
    back_block_id = db.Column(db.Integer, db.ForeignKey('block.id'))

    front_block = db.relationship('Block', foreign_keys=[front_block_id])
    back_block = db.relationship('Block', foreign_keys=[back_block_id])

    def _repr_(self):
        return "<Train {}>".format(repr(self.id))
