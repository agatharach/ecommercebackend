import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from sqlalchemy import desc
from .model import Users
from blueprints import db, app
from blueprints import internal_required


bp_user = Blueprint('user',__name__)
api = Api(bp_user)

class UserGetResource(Resource):
    def options(self):
        return {'status' :'ok'},200
        
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        id = claims['id']
        qry = Users.query.get(id)
        if qry is not None:
            return marshal(qry, Users.response_fields),200, {'Content-Type': 'application/json'}
        return {'status': 'NOT FOUND', 'message': 'Person not found'}, 404

    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json')
        parser.add_argument('password', location='json')
        parse.add_argument('alamat', location='json')
        parser.add_argument('status', location='json')
        parser.add_argument('nomorhp', location='json')
        args = parser.parse_args()

        qry = Users.query.get(id)
        if qry is None:
            return {'status': "NOT_FOUND"}, 404

        qry.username = args['username']
        qry.password = args['password']
        qry.status = args['status']
        qry.alamat = args['alamat']
        qry.nomorhp = args['nomorhp']


        return marshal(qry, Users.response_fields), 200

    def delete(self, id=None):
        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()
        
        return {'status': 'DELETED'}, 200


class UserResource(Resource):
    def options(self):
        return {'status' :'ok'},200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json')
        parser.add_argument('password', location='json')        
        parser.add_argument('alamat', location='json')
        parser.add_argument('status', location='json', default=1)
        parser.add_argument('nomorhp', location='json')

        data = parser.parse_args()

        user = Users(data['username'], data['password'], data['alamat'], data ['status'], data ['nomorhp'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)
        return marshal(user, Users.response_fields),200,{'Content-Type': 'application/json'}  
  
    

class CreateTokenResource(Resource):
    def options(self):
        return {'status' :'ok'},200
    
    # for login auth
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args')
        parser.add_argument('password', location='args')
        data = parser.parse_args()

        qry = Users.query
        userData = qry.filter_by(username=data['username']).filter_by(password=data['password']).first()

        if userData is not None:
            userData = marshal(userData, Users.response_fields)
            userData.pop('password')
            token = create_access_token(identity=data['username'], user_claims=userData)
            return {'token':token},200,{'Content-Type': 'application/json'} 
        else :
            return {'status':'UNAUTHORIZED', 'MESSAGE':'SALAH ID'},401


class UserList(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25) 
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('asc','desc'))
        args = parser.parse_args()

        offset = (args['p']*args['rp'])-args['rp']

        qry = Users.query

        if args['sort'] is not None:
            if args['sort']=='asc':
                qry.order_by(Users.username)
            else:
                qry.order_by(desc(Users.username))
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_fields))
        
        return rows, 200, {'Content-Type': 'application/json'}

api.add_resource(UserList, '/list')
api.add_resource(CreateTokenResource, '/login')
api.add_resource(UserGetResource,'/whoisme')
api.add_resource(UserResource,'')
