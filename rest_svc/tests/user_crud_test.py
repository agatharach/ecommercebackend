import json
from . import app, client, cache, create_token

class TestUsersCrud():
    var = 0
    def test_User_valid_input_post_name(self, client):
        data = {
            'username':'agatha',
            'password':'iopklm',
            'alamat':'jalan kesana kemari',
            'status': 1
            'nomorhp': '0896283492729'
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/users', data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        TestUserCrud.var = res_json['id']
        assert res.status_code == 200
    
    def test_User_invalid_post_name(self, client):
        data = {
            'client_secret':'SECRET08',
            'status':True,
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/daftar', data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_User_getlist(self, client): # client dr init test
        res = client.get('/users/list',
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_invalid_User_getlist(self, client): # client dr init test
        res = client.get('/users/list1',
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404
    

    def test_User_get_valid_id_token(self, client):
        res = client.get('/daftar/'+str(TestUserCrud.var))
        
        res_json = json.loads(res.data)
        assert res.status_code == 200


    def test_User_get_invalid_id_token(self, client):
        res = client.get('/daftar/25',
                        headers={'Authorization':'Bearer abc'})
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    

    def test_User_valid_put_token(self, client):
        token = create_token()
        data = {
            'client_key':'CLIENT10',
            'client_secret':'SECRET10',
            'status':True,
        }
        res = client.put('/daftar/'+str(TestClientCrud.var),
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 400


    def test_User_invalid_put_token(self, client):
        token = create_token()
        data = {
            'client_secret':'SECRET10',
            'status':True,
        }
        res = client.put('/daftar/15',
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_User_valid_delete_token(self, client):
        token = create_token()
        res = client.delete('/daftar/'+str(TestClientCrud.var),
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200


    def test_User_invalid_delete_token(self, client):
        token = create_token()
        res = client.delete('/daftar/12',
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

