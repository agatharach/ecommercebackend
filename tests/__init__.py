import pytest, json, logging
from flask import Flask, request
from blueprints import app,db, cache
from blueprints.user.model import Users as UserModel



def call_client(request):
    client = app.test_client()
    return client


@pytest.fixture
def client(request):
    return call_client(request)


def reset_database():

    db.drop_all()
    db.create_all()
    # create test non-admin user
    user = UserModel("agathar","iopklm","jl joko kandung 136",0,"08953797508")
    penjual = UserModel("tania", "weqryqa","jl. cisitu indah baru no. 6", 1, "087615729131" )
    # save users to database
    db.session.add(user)
    db.session.add(penjual)
    db.session.commit()

def create_token():
    token = cache.get('test-token')
    if token is None:
        ##prepare request input
        data = {'username': 'agathar', 'password': 'iopklm'}
        # do request
        req = call_client(request)
        res = req.get('/users/login',
                      query_string=data,
                      content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)
        # assert if the result is as expected
        assert res.status_code == 200

        # save token into cache
        cache.set('test_token', res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token


def create_token_penjual():
    token = cache.get('test-token')
    if token is None:
        ##prepare request input
        data = {'username': 'tania', 'password': 'weqryqa'}
        # do request
        req = call_client(request)
        res = req.get('/users/login',
                      query_string=data,
                      content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)
        # assert if the result is as expected
        assert res.status_code == 200

        # save token into cache
        cache.set('test_token', res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token