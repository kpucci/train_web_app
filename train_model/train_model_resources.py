from flask_restful import Resource, fields, reqparse, marshal_with, inputs
from flask import request, abort, flash, jsonify, json
from models import db, Block, Train, Message

trainLength = 1000.0
trainHeight = 100.0
trainWidth = 100.0
trainMass = 1000.0

train_fields = {
    'id': fields.Integer,
	'name': fields.String,
    'speed': fields.Float,
    'authority': fields.String,
    'length': fields.Float,
    'width': fields.Float,
    'height': fields.Float,
    'mass': fields.Float,
    'crewCount': fields.Integer,
    'passengerCount': fields.Integer,
    'front_block_id': fields.Integer,
    'back_block_id': fields.Integer
}

add_train_parser = reqparse.RequestParser(bundle_errors=True)
add_train_parser.add_argument('name', type=str, required=True, location='json')

update_train_parser = reqparse.RequestParser(bundle_errors=True)
update_train_parser.add_argument('speed', type=float, location='json')
update_train_parser.add_argument('authority', type=str, location='json')
update_train_parser.add_argument('crewCount', type=int, location='json')
update_train_parser.add_argument('passengerCount', type=int, location='json')
update_train_parser.add_argument('front_block_id', type=int, location='json')
update_train_parser.add_argument('back_block_id', type=int, location='json')

class TrainResource(Resource):
    @marshal_with(train_fields)
    def get(self, id):
        train = Train.query.filter_by(id=id).first()

        if not train:
            print("Train %d: not found." % id)
            abort(404, "Train %d: not found." % id)

        return train

    @marshal_with(train_fields)
    def put(self, id):
        train = Train.query.filter_by(id=id).first()

        if not train:
            print("Train %d: not found." % id)
            abort(404, "Train %d: not found." % id)

        train_args = update_train_parser.parse_args()
        if "speed" in train_args:
            train.speed = train_args['speed']
        if "authority" in train_args:
            train.authority = train_args['authority']
        if "crewCount" in train_args:
            train.crewCount = train_args['crewCount']
        if "passengerCount" in train_args:
            train.passengerCount = train_args['passengerCount']

        if train_args['front_block_id'] is not None:
            front_block = Block.query.filter_by(id=int(train_args['front_block_id'])).first()
            if not front_block:
                print("Block %d: not found." % id)
                abort(404, "Block %d: not found." % id)
            train.front_block = front_block
            front_block_msg = front_block.message
            front_block_msg.train = train
            train.message = front_block_msg

        if train_args['back_block_id'] is not None:
            back_block = Block.query.filter_by(id=int(train_args['back_block_id'])).first()
            if not back_block:
                print("Block %d: not found." % id)
                abort(404, "Block %d: not found." % id)
            train.back_block = back_block

        db.session.commit()

        return train, 201

class TrainListResource(Resource):
    @marshal_with(train_fields)
    def get(self):
        trains = Train.query.all()
        return trains

    @marshal_with(train_fields)
    def post(self):
        train_args = add_train_parser.parse_args()
        ordered = Train.query.order_by(Train.id.desc()).all()
        if ordered and Train.query.filter_by(name=train_args['name']).first():
            abort(400, 'Train %s already exists. Please choose a new name.' % train_args['name'])

        if 'id' not in train_args:
            if ordered:
                highest = ordered[0].id
            else:
                highest = 0
            train_id = highest + 1
        else:
            train_id = train_args['id']

        train = Train(id=train_id,name=train_args['name'])
        train.speed = 0.0
        train.length = trainLength
        train.width = trainWidth
        train.height = trainHeight
        train.mass = trainMass
        train.crewCount = 0
        train.passengerCount = 0

        db.session.add(train)
        db.session.commit()

        return train, 201
