from flask_restful import Resource, fields, reqparse, marshal_with, inputs
from flask import request, abort, flash, jsonify, json
from models import db, CTCRequest

ctc_request_fields = {
    'type': fields.Integer,
    'input': fields.String
}

ctc_request_parser = reqparse.RequestParser(bundle_errors=True)
ctc_request_parser.add_argument('type', type=int, required=True, location='json')
ctc_request_parser.add_argument('input', type=str, required=True, location='json')

class CTCRequestResource(Resource):
    @marshal_with(ctc_request_fields)
    def get(self):
        request = CTCRequest.query.first()
        return request

    @marshal_with(ctc_request_fields)
    def put(self):
        request = CTCRequest.query.first()

        if not request:
            abort(404, "Request not found.")

        ctc_request_args = ctc_request_parser.parse_args()
        request.type = ctc_request_args['type']
        request.input = ctc_request_args['input']

        db.session.commit()

        return request, 201
