from flask_restful import Resource, fields, reqparse, marshal_with, inputs
from flask import request, abort, flash, jsonify, json
from models import db, Block, Station, Switch, Crossing, Light, Train

trainLength = 1000.0
trainHeight = 100.0
trainWidth = 100.0
trainMass = 1000.0

block_fields = {
	'id': fields.Integer,
    'number': fields.Integer,
    'line': fields.String,
    'grade': fields.Float,
    'elevation': fields.Float,
    'cumulative_elevation': fields.Float,
    'occupancy': fields.Boolean,
    'switch_id': fields.Integer,
    'station_id': fields.Integer,
    'crossing_id': fields.Integer,
    'message': fields.String
}

station_fields = {
    'id': fields.Integer,
	'name': fields.String,
	'block_id': fields.Integer
}

switch_fields = {
    'id': fields.Integer,
	'state': fields.Boolean,
	'block_id': fields.Integer
}

crossing_fields = {
    'id': fields.Integer,
	'state': fields.Boolean,
	'block_id': fields.Integer
}

light_fields = {
    'id': fields.Integer,
	'state': fields.Boolean,
	'switch_id': fields.Integer,
    'crossing_id': fields.Integer
}

train_fields = {
    'id': fields.Integer,
	'name': fields.String,
    'speed': fields.Float,
    'length': fields.Float,
    'width': fields.Float,
    'height': fields.Float,
    'mass': fields.Float,
    'crewCount': fields.Integer,
    'passengerCount': fields.Integer,
    'front_block_id': fields.Integer,
    'back_block_id': fields.Integer
}

message_fields = {
    'message': fields.String
}

add_block_parser = reqparse.RequestParser(bundle_errors=True)
add_block_parser.add_argument('id', type=int, location='json')
add_block_parser.add_argument('number', type=int, required=True, location='json')
add_block_parser.add_argument('line', type=str, required=True, location='json')
add_block_parser.add_argument('grade', type=float, location='json')
add_block_parser.add_argument('elevation', type=float, location='json')
add_block_parser.add_argument('cumulative_elevation', type=float, location='json')
add_block_parser.add_argument('occupancy', type=inputs.boolean, location='json')
add_block_parser.add_argument('switch_id', type=int, location='json')
add_block_parser.add_argument('station_id', type=int, location='json')
add_block_parser.add_argument('crossing_id', type=int, location='json')

update_block_parser = reqparse.RequestParser(bundle_errors=True)
update_block_parser.add_argument('id', type=int, location='json')
update_block_parser.add_argument('occupancy', type=inputs.boolean, required=True, location='json')

station_parser = reqparse.RequestParser(bundle_errors=True)
station_parser.add_argument('id', type=int, location='json')
station_parser.add_argument('name', type=str, required=True, location='json')
station_parser.add_argument('block_id', type=int, required=True, location='json')

switch_parser = reqparse.RequestParser(bundle_errors=True)
switch_parser.add_argument('id', type=int, location='json')
switch_parser.add_argument('state', type=inputs.boolean, required=True, location='json')
switch_parser.add_argument('block_id', type=int, required=True, location='json')

crossing_parser = reqparse.RequestParser(bundle_errors=True)
crossing_parser.add_argument('id', type=int, location='json')
crossing_parser.add_argument('state', type=inputs.boolean, required=True, location='json')
crossing_parser.add_argument('block_id', type=int, required=True, location='json')

light_parser = reqparse.RequestParser(bundle_errors=True)
light_parser.add_argument('id', type=int, location='json')
light_parser.add_argument('state', type=inputs.boolean, required=True, location='json')
light_parser.add_argument('switch_id', type=int, location='json')
light_parser.add_argument('crossing_id', type=int, location='json')

add_train_parser = reqparse.RequestParser(bundle_errors=True)
add_train_parser.add_argument('name', type=str, required=True, location='json')

update_train_parser = reqparse.RequestParser(bundle_errors=True)
update_train_parser.add_argument('speed', type=float, location='json')
update_train_parser.add_argument('crewCount', type=int, location='json')
update_train_parser.add_argument('passengerCount', type=int, location='json')

message_parser = reqparse.RequestParser(bundle_errors=True)
message_parser.add_argument('message', type=str, location='json')

class BlockResource(Resource):
    @marshal_with(block_fields)
    def get(self, id):
        # block = Block.query.filter((Block.number==number) & (Block.line==line)).first()
        block = Block.query.filter_by(id=id).first()

        if not block:
            abort(404, "Block %d: not found." % id)

        return block

    @marshal_with(block_fields)
    def put(self, id):
        block_args = update_block_parser.parse_args()
        block = Block.query.filter_by(id=id).first()

        if not block:
            abort(404, "Block %d: not found." % id)

        block.occupancy = block_args['occupancy']

        db.session.commit()

        return block, 201

class BlockListResource(Resource):
    @marshal_with(block_fields)
    def get(self):
        blocks = Block.query.all()
        return blocks

    @marshal_with(block_fields)
    def post(self):
        block_args = add_block_parser.parse_args()

        if 'id' not in block_args:
            highest = Block.query.order_by(Block.id).last()
            block_id = highest + 1
        else:
            block_id = block_args['id']

        block = Block(id=block_id, number=block_args['number'], line=block_args['line'],
            grade=block_args['grade'], elevation=block_args['elevation'], cumulative_elevation=block_args['cumulative_elevation'],
            occupancy=block_args['occupancy'])

        if 'switch_id' in block_args:
            block.switch_id = block_args['switch_id']

        if 'station_id' in block_args:
            block.station_id = block_args['station_id']

        if 'crossing_id' in block_args:
            block.crossing_id = block_args['crossing_id']

        db.session.add(block)
        db.session.commit()

        return block, 201

class StationResource(Resource):
    @marshal_with(station_fields)
    def get(self, name):
        station = Station.query.filter_by(name=name).first()

        if not station:
            abort(404, "Station %s: not found." % name)

        return station

class StationListResource(Resource):
    @marshal_with(station_fields)
    def get(self):
        stations = Station.query.all()

        return stations

    @marshal_with(station_fields)
    def post(self):
        station_args = station_parser.parse_args()

        if 'id' not in station_args:
            highest = Station.query.order_by(Station.id).last()
            station_id = highest + 1
        else:
            station_id = station_args['id']

        station = Station(id=station_id,name=station_args['name'],block_id=station_args['block_id'])
        block = Block.query.filter_by(id=station_args['block_id']).first()
        if not block:
            abort(404, "Block %d: not found." % station_args['block_id'])

        block.station_id = station_id

        db.session.add(station)
        db.session.commit()

        return station, 201

class SwitchResource(Resource):
    @marshal_with(switch_fields)
    def get(self, id):
        switch = Switch.query.filter_by(id=id).first()

        if not switch:
            abort(404, "Switch %d: not found." % id)

        return switch

    @marshal_with(switch_fields)
    def put(self, id):
        switch_args = switch_parser.parse_args()
        switch = Switch.query.filter_by(id=id).first()

        if not switch:
            abort(404, "Switch %d: not found." % id)

        switch.state = switch_args['state']

        db.session.commit()

        return switch

class SwitchListResource(Resource):
    @marshal_with(switch_fields)
    def get(self):
        switches = Switch.query.all()
        return switches

    @marshal_with(switch_fields)
    def post(self):
        switch_args = switch_parser.parse_args()

        if 'id' not in switch_args:
            highest = Switch.query.order_by(Switch.id).last()
            switch_id = highest + 1
        else:
            switch_id = switch_args['id']

        switch = Switch(id=switch_id,state=switch_args['state'],block_id=switch_args['block_id'])
        block = Block.query.filter_by(id=switch_args['block_id']).first()
        if not block:
            abort(404, "Block %d: not found." % switch_args['block_id'])
        block.switch_id = switch_id

        db.session.add(switch)
        db.session.commit()

        return switch, 201

class CrossingResource(Resource):
    @marshal_with(crossing_fields)
    def get(self, id):
        crossing = Crossing.query.filter_by(id=id).first()

        if not crossing:
            abort(404, "Crossing %d: not found." % id)

        return crossing

    @marshal_with(crossing_fields)
    def put(self, id):
        crossing_args = crossing_parser.parse_args()
        crossing = Crossing.query.filter_by(id=crossing_args['id']).first()

        if not crossing:
            abort(404, "Crossing %d: not found." % id)

        crossing.state = crossing_args['state']

        db.session.commit()

        return crossing

class CrossingListResource(Resource):
    @marshal_with(crossing_fields)
    def get(self):
        crossings = Crossing.query.all()
        return crossings

    @marshal_with(crossing_fields)
    def post(self):
        crossing_args = crossing_parser.parse_args()

        if 'id' not in crossing_args:
            highest = Crossing.query.order_by(Crossing.id).last()
            crossing_id = highest + 1
        else:
            crossing_id = crossing_args['id']

        crossing = Crossing(id=switch_id,state=crossing_args['state'],block_id=crossing_args['block_id'])
        block = Block.query.filter_by(id=crossing_args['block_id']).first()
        if not block:
            abort(404, "Block %d: not found." % crossing_args['block_id'])
        block.crossing_id = crossing_id

        db.session.add(crossing)
        db.session.commit()

        return crossing, 201

class LightResource(Resource):
    @marshal_with(light_fields)
    def get(self, id):
        light = Light.query.filter_by(id=id).first()

        if not light:
            abort(404, "Light %d: not found." % id)

        return light

class LightListResource(Resource):
    @marshal_with(light_fields)
    def get(self):
        lights = Light.query.all()
        return lights

    @marshal_with(light_fields)
    def post(self):
        light_args = light_parser.parse_args()

        if 'id' not in light_args:
            highest = Light.query.order_by(Light.id).last()
            light_id = highest + 1
        else:
            light_id = light_args['id']

        light = Light(id=light_id,state=light_args['state'])

        if 'switch_id' in light_args:
            light.switch_id = light_args['switch_id']
            switch = Switch.query.filter_by(id=light_args['switch_id']).first()
            if not switch:
                abort(404, "Switch %d: not found." % light_args['switch_id'])
            switch.lights.append(light)
        elif 'crossing_id' in light_args:
            light.crossing_id = light_args['crossing_id']
            crossing = Crossing.query.filter_by(id=light_args['crossing_id']).first()
            if not crossing:
                abort(404, "Crossing %d: not found." % light_args['crossing_id'])
            crossing.lights.append(light)
        else:
            abort(400, "A light object requires either a switch id or a crossing id")

        db.session.add(light)
        db.session.commit()

        return light, 201

class TrainResource(Resource):
    @marshal_with(train_fields)
    def get(self, id):
        train = Train.query.filter_by(id=id).first()

        if not train:
            abort(404, "Train %d: not found." % id)

        return train

    @marshal_with(train_fields)
    def put(self, id):
        train = Train.query.filter_by(id=id).first()

        if not train:
            abort(404, "Train %d: not found." % id)

        train_args = update_train_parser.parse_args()
        train.speed = train_args['speed']
        train.blocks = []
        for block in train_args['blocks']:
            block = Block.query.filter_by(id=block).first()
            train.blocks.append(block)

        db.session.commit()

        return switch

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

class MessageResource(Resource):
    @marshal_with(message_fields)
    def get(self, id):
        block = Block.query.filter_by(id=id).first()

        if not block:
            abort(404, "Block %d: not found." % id)


        return block, 200

    @marshal_with(message_fields)
    def put(self, id):
        block = Block.query.filter_by(id=id).first()

        if not block:
            abort(404, "Block %d: not found." % id)

        message_args = message_parser.parse_args()
        block.message = message_args['text']

        db.session.commit()

        return block, 201
