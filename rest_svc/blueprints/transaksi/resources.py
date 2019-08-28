import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Trx
from blueprints.barang.model import Barangs 
from blueprints import db, app
from flask_jwt_extended import jwt_required
from blueprints import internal_required



bp_transaksi = Blueprint('transaksi',__name__)
api = Api(bp_transaksi)

class TransaksiResource(Resource):
    def options(self,id):
        return {'status' :'ok'},200
        
    @jwt_required
    def get(self, id):
        qry = Trx.query.filter_by(user_id=id)
        if qry is not None:
            rows = []
            for row in qry.all():
                rows.append(marshal(row, Trx.response_fields))
            return rows,200
        return {'status': 'NOT FOUND', 'message': 'Cart not found'}, 404

class EditTransaksiStatus(Resource):
    def options(self):
        return {'status' :'ok'},200
    
    @jwt_required
    @internal_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json')
        parser.add_argument('status', location='json')
        data = parser.parse_args()

        transaksi = Trx.query.filter_by(id=data['user_id'])

        if transaksi is not None:
            for row in transaksi.all():
                transaksi.status = data['status']
                db.session.commit()
            return marshal(transaksi,Trx.response_fields),200   
        else :
            return {'status': 'NOT FOUND', 'message': 'Person not found'}, 404
            
api.add_resource(TransaksiResource,'/<id>')
api.add_resource(EditTransaksiStatus,'/status')

    