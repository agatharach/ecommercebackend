import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Carts
from blueprints.barang.model import Barangs
from blueprints.transaksi.model import Trx
from blueprints.user.model import Users
from blueprints.barang.model import Barangs
from blueprints import db, app
from flask_jwt_extended import jwt_required
from blueprints import internal_required


bp_cart = Blueprint('cart',__name__)
api = Api(bp_cart)

class CartResource(Resource):
    def options(self,id):
        return {'status' :'ok'},200
    
    @jwt_required
    def get(self, id):
        qry = Carts.query.filter_by(user_id=id)
        if qry is not None:
            rows = []
            for row in qry.all():
                rows.append(marshal(row, Carts.response_fields))
            return rows,200
        return {'status': 'NOT FOUND', 'message': 'Cart not found'}, 404
    
class CartResourcePlus(Resource):
    def options(self,id):
        return {'status' :'ok'},200
    @jwt_required
    def put(self,id):
        parser = reqparse.RequestParser()        
        parser.add_argument('user_id', location='json')
        data = parser.parse_args()
        
        qry = Carts.query
        cartData = qry.filter_by(user_id=data['user_id']).filter_by(barang_id=id).first()
        if cartData is None:
            return {'status': 'NOT FOUND', 'message': 'Cart not found'}, 404, {'Content-Type': 'application/json'}
        
        jumlah_old = marshal(cartData,Carts.response_fields)['jumlah']
        cartData.jumlah = jumlah_old+1
        jumlah_new = marshal(cartData,Carts.response_fields)['jumlah']

        itemsData = Barangs.query.filter_by(barang_id=id).first()        
        stok = marshal(itemsData,Carts.response_fields)['stok']

        if jumlah_new > stok :
            return {'status': 'ERROR', 'message': 'Jumlah out of range'}, 404, {'Content-Type': 'application/json'} 
        else :
             db.session.commit()
        return marshal(cartData,Carts.response_fields),200

        db.session.commit()
        return marshal(cartData,Carts.response_fields),200

class CartResourceMinus(Resource):
    def options(self,id):
        return {'status' :'ok'},200
        
    @jwt_required
    def put(self,id):
        parser = reqparse.RequestParser()        
        parser.add_argument('user_id', location='json')
        data = parser.parse_args()
        
        qry = Carts.query
        cartData = qry.filter_by(user_id=data['user_id']).filter_by(barang_id=id).first()
        if cartData is None:
            return {'status': 'NOT FOUND', 'message': 'Cart not found'}, 404, {'Content-Type': 'application/json'}
        
        jumlah_old = marshal(cartData,Carts.response_fields)['jumlah']
        cartData.jumlah = jumlah_old-1
        jumlah_new = marshal(cartData,Carts.response_fields)['jumlah']
        if jumlah_new < 0 :
            return {'status': 'ERROR', 'message': 'Jumlah out of range'}, 404, {'Content-Type': 'application/json'} 
        else :
             db.session.commit()
        return marshal(cartData,Carts.response_fields),200

class CartDeleteItems(Resource) :
    def options(self,id):
        return {'status' :'ok'},200
    @jwt_required
    def delete(self,id):
        parser = reqparse.RequestParser()        
        parser.add_argument('user_id', location='json')
        data = parser.parse_args()

        qry = Carts.query
        cartData = qry.filter_by(user_id=data['user_id']).filter_by(barang_id=id).first()

        if cartData is None:
            return {'status': 'NOT FOUND', 'message': 'Cart not found'}, 404, {'Content-Type': 'application/json'}
        
        db.session.delete(cartData)
        db.session.commit()
        return {'status' : 'Deleted'},200

class CartCheckout(Resource):
    def options(self):
        return {'status' :'ok'},200
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json')
        parser.add_argument('status', location='json')
        parser.add_argument('metodebayar', location='json')
        parser.add_argument('kurir', location='json')        
        data = parser.parse_args()

        cartData = Carts.query.filter_by(user_id=data['user_id'])
        userData = Users.query.filter_by(id=data['user_id']).first()
        if cartData is not None:
            for row in cartData.all():
                barang_id = marshal(row, Carts.response_fields)['barang_id']
                user_id = marshal(row, Carts.response_fields)['user_id']
                jumlah = marshal(row, Carts.response_fields)['jumlah']
                nama = marshal(userData, Users.response_fields)['username']
                alamat = marshal(userData, Users.response_fields)['alamat']
                nomorhp = marshal(userData, Users.response_fields)['nomorhp']
                itemsData = Barangs.query.filter_by(id=barang_id).first()
                harga = marshal(itemsData,Barangs.response_fields)['harga']
                totalharga = jumlah*harga
                stok_lama=marshal(itemsData,Barangs.response_fields)['stok']
                itemsData.stok = int(stok_lama)-jumlah
                db.session.commit()


                transaksi = Trx(barang_id,user_id,jumlah,nama,alamat,nomorhp,data['status'],totalharga,data['metodebayar'],data['kurir'])
                db.session.add(transaksi)
                db.session.commit()

                db.session.delete(row)
                db.session.commit()

                app.logger.debug('DEBUG : %s', transaksi)
            
        else :
            return {'status': 'NOT FOUND', 'message': 'Cart not found'}, 404, {'Content-Type': 'application/json'}
        return {'status' :'ok'},200
            


api.add_resource(CartResource,'/<id>')
api.add_resource(CartResourcePlus,'/plusjumlah/<id>')
api.add_resource(CartResourceMinus,'/minusjumlah/<id>')
api.add_resource(CartDeleteItems,'/deletecart/<id>')
api.add_resource(CartCheckout,'/checkout')