import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from sqlalchemy import desc
from .model import Barangs
from blueprints.cart.model import Carts
from blueprints import db, app
from flask_jwt_extended import jwt_required
from blueprints import internal_required

bp_barang = Blueprint('barang', __name__)
api = Api(bp_barang)


class BarangResource(Resource):
    def options(self, id):
        return {'status': 'ok'}, 200

    def get(self, id):
        qry = Barangs.query.get(id)
        if qry is not None:
            return marshal(qry, Barangs.response_fields), 200
        return {'status': 'NOT FOUND', 'message': 'Items not found'}, 404

    @jwt_required
    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json')
        data = parser.parse_args()

        qry = Carts.query
        cartData = qry.filter_by(user_id=data['user_id']).filter_by(
            barang_id=id).first()

        if cartData is None:
            jumlah = 1
            cart = Carts(id, data['user_id'], jumlah)
            db.session.add(cart)
            db.session.commit()

            app.logger.debug('DEBUG : %s', cart)
            return marshal(cart, Carts.response_fields), 200

        else:
            jumlah_lama = marshal(cartData, Carts.response_fields)['jumlah']
            cartData.jumlah = jumlah_lama + 1
            db.session.commit()
            return marshal(cartData, Carts.response_fields), 200

    @jwt_required
    @internal_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json')
        parser.add_argument('username', location='json')
        parser.add_argument('name', location='json')
        parser.add_argument('stok', location='json')
        parser.add_argument('harga', location='json')
        parser.add_argument('category', location='json')
        parser.add_argument('urlfoto', location='json')
        parser.add_argument('deskripsi', location='json')
        
        qry = Barangs.query.get(id)
        
        if qry is None:
            return {'status': "NOT_FOUND"}, 404

        body = parser.parse_args()
        
        qry.user_id = body['user_id']
        qry.username = body['username']
        qry.name = body['name']
        qry.stok = body['stok']
        qry.harga = body['harga']
        qry.category = body['category']
        qry.urlfoto = body['urlfoto']
        qry.deskripsi = body['deskripsi']

        db.session.commit()

        return marshal(qry, Barangs.response_fields)

    @jwt_required
    @internal_required
    def delete(self, id):
        qry = Barangs.query.get(id)
        if qry is None:
            return {
                'status': 'NOT FOUND',
                'message': 'Person not found'
            }, 404, {
                'Content-Type': 'application/json'
            }
        
        db.session.delete(qry)
        db.session.commit()
        
        return {'status': 'Deleted'}, 200

class BarangPost(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json')
        parser.add_argument('username', location='json')
        parser.add_argument('name', location='json')
        parser.add_argument('stok', location='json')
        parser.add_argument('harga', location='json')
        parser.add_argument('category', location='json')
        parser.add_argument('urlfoto', location='json')
        parser.add_argument('deskripsi', location='json')

        data = parser.parse_args()

        barang = Barangs(data['user_id'], data['username'], data['name'],
                         data['stok'], data['harga'], data['category'],
                         data['urlfoto'], data['deskripsi'])
        
        db.session.add(barang)
        db.session.commit()

        app.logger.debug('DEBUG : %s', barang)
        return marshal(barang, Barangs.response_fields)


class BarangList(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=10)
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Barangs.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Barangs.response_fields))

        return rows, 200, {'Content-Type': 'application/json'}

api.add_resource(BarangList, '/list')
api.add_resource(BarangResource, '/list/<id>')
api.add_resource(BarangPost, '/tambah')
