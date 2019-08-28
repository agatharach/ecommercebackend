import pytest, json, logging
from flask import Flask, request
from blueprints import app
from app import cache

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token():
    token = cache.get('test-token')
    if token is None:
        ##prepare request input
        data = {
            'username' : 'agathar',
            'password' : 'iopklm'
        }
        # do request
        req = call_client(request)
        res = req.get('/users/login', query_string=data, content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)
        # assert if the result is as expected
        assert res.status_code == 200

        # save token into cache
        cache.set('test_token',res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token

def create_token_penjual():
    token = cache.get('test-token')
    if token is None:
        ##prepare request input
        data = {
            'username' : 'tania',
            'password' : 'weqryqa'
        }
        # do request
        req = call_client(request)
        res = req.get('/users/login', query_string=data, content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)
        # assert if the result is as expected
        assert res.status_code == 200

        # save token into cache
        cache.set('test_token',res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token