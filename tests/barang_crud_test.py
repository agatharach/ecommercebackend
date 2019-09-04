import json
from . import app, client, cache, create_token, create_token_penjual, reset_database
import sys

sys.path.append('path')

class TestUsersCrud():
    userid = 0
    reset_database()

    def test_user_valid_input_post_name(self, client):
        data = {
            'username': 'agatha',
            'password': 'iopklm',
            'alamat': 'jalan kesana kemari',
            'status': 1,
            'nomorhp': '0896283492729'
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/users',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        TestUsersCrud.userid = res_json['id']
        assert res.status_code == 200

    # def test_user_invalid_post_name(self, client):
    #     data = {
    #         'username': 'agatha',
    #         'password': 'iopklm'
    #     }
    #     #karena post menggunakan data, sedangkan get menggunakan query_string
    #     res = client.post('/users',
    #                       data=json.dumps(data),
    #                       content_type='application/json')

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 500

    def test_user_getlist(self, client):  # client dr init test
        res = client.get('/users/list', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_invalid_user_getlist(self, client):  # client dr init test
        res = client.get('/users/list1', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 422

    def test_user_get_valid_id_token(self, client):
        token = create_token()
        res = client.get('/users/whoisme',
                         headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_get_invalid_id_token(self, client):
        res = client.get('/users/whoisme',
                         headers={'Authorization': 'Bearer abc'})

        res_json = json.loads(res.data)
        assert res.status_code == 500

    def test_user_valid_put_token(self, client):
        token = create_token()
        data = {
            'username': 'agatha1',
            'password': 'iopklmy',
            'alamat': 'jalan jalan sore',
            'status': 1,
            'nomorhp': '0896283492729'
        }
        res = client.put('/users/whoisme/' + str(TestUsersCrud.userid),data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_invalid_put_token(self, client):
        token = create_token()
        data = {
            'username': 'agatha12',
            'password': 'iopklmy',
            'alamat': 'jalan jalan sore',
            'status': 1,
            'nomorhp': '0896283492729'
        }
        res = client.put('/users/whoisme/15',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_user_valid_delete_token(self, client):
        token = create_token()
        res = client.delete('/users/whoisme/' + str(TestUsersCrud.userid),
                            headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_invalid_delete_token(self, client):
        token = create_token()
        res = client.delete('/users/whoisme/12',
                            headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_user_valid_option(self, client):
        res = client.options('/users/whoisme')

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_user_valid_option_resource(self, client):
        res = client.options('/users')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_valid_option_token(self, client):
        res = client.options('/users/login')

        res_json = json.loads(res.data)
        assert res.status_code == 200

class TestBarangCrud():
    idbarang = 0

    def test_barang_valid_input_post_name(self, client):
        token = create_token_penjual()
        data = {
            "user_id": 2,
            "username":'Arataaaa Beras Supplier',
            'name':'Beras Basmati High Quality',
            'stok':5,
            'harga':25000,
            'category':'500gram',
            'urlfoto':'',
            'deskripsi':'Beras khas India yang diimpor langsung dari negara asalnya. Dijual murah karena butuh uang.'
        } 

        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/items/tambah',
                          data=json.dumps(data),
                          headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        TestBarangCrud.idbarang = res_json['id']
        assert res.status_code == 200

    def test_barang_invalid_post_name(self, client):
        data = {'user_id': 5, 'username': 'Arata Beras Supplier'}
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/items/tambah',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 500

    def test_barang_getlist(self, client):  # client dr init test
        res = client.get('/items/list', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_invalid_barang_getlist(self, client):  # client dr init test
        res = client.get('/items/list1', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_barang_get_valid(self, client):
        res = client.get('/items/list/' + str(TestBarangCrud.idbarang))

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_barang_get_invalid_id(self, client):
        res = client.get('/items/list/30', content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_barang_valid_put_token(self, client):
        token = create_token_penjual()
        data = {
            'user_id':2,
            'username':'Arataaaaaa Beras w',
            'name':'Beras Basmati High Quality Banget',
            'stok':5,
            'harga':25000,
            'category':'500gram',
            'urlfoto':'',
            'deskripsi':'Beras khas India yang diimpor langsung dari negara asalnya. Dijual murah karena butuh uang.'
        }
        res = client.put('/items/list/' + str(TestBarangCrud.idbarang),
                       data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_barang_invalid_put_token(self, client):
        token = create_token_penjual()
        data = {
            'user_id':2,
            'username':'Arataaaa Beras w',
            'name':'Beras Basmati High Quality Banget',
            'stok':5,
            'harga':25000,
            'category':'500gram',
            'urlfoto':'',
            'deskripsi':'Beras khas India yang diimpor langsung dari negara asalnya. Dijual murah karena butuh uang.'

        }
        res = client.put('/items/list/100',
                       data=json.dumps(data),headers={'Authorization': 'Bearer ' + token},content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_barang_valid_delete_token(self, client):
        token = create_token()
        res = client.delete('/items/list/' + str(TestBarangCrud.idbarang),
                         headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_barang_invalid_delete_token(self, client):
        token = create_token()
        res = client.delete('/items/list/12',
                            headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 403

    def test_baranglist_valid_option(self, client):
        res = client.options('/items/list')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_barangresource_valid_option(self, client):
        res = client.options('/items/list/'+  str(TestBarangCrud.idbarang))

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_barang_valid_option(self, client):
        res = client.options('/items/tambah')

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    
class TestCartCrud():
    idcart = 0

    def test_cart_valid_post(self, client):
        token = create_token()
        data = {
            'user_id' : 1
        }
        res = client.post('/items/list/'+ str(TestBarangCrud.idbarang),
        data=json.dumps(data),
        headers={'Authorization': 'Bearer ' + token}
        ,content_type='application/json')

        res_json = json.loads(res.data)
        TestCartCrud.idcart = res_json['id']
        assert res.status_code == 200
    
    def test_cartelse_valid_post(self, client):
        token = create_token()
        data = {
            'user_id' : 1
        }
        res = client.post('/items/list/'+ str(TestBarangCrud.idbarang),
        data=json.dumps(data),
        headers={'Authorization': 'Bearer ' + token}
        ,content_type='application/json')

        res_json = json.loads(res.data)
        TestCartCrud.idcart = res_json['id']
        assert res.status_code == 200

    def test_cart_valid_input_post(self, client):
        token = create_token()
        data = {
            "user_id": 1,
            "status":'PENDING',
            'metodebayar':'TRANSFER',
            'kurir':"JNT"} 

        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/carts/checkout',
                          data=json.dumps(data),
                          headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        TestCartCrud.idcart = res_json['id']
        assert res.status_code == 200
    
    def test_cart_valid_postelse(self, client):
        token = create_token()
        data = {
            "user_id": 100,
            "status":'PENDING',
            'metodebayar':'TRANSFER',
            'kurir':"JNT"} 

        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/carts/checkout',
                          data=json.dumps(data),
                          headers={'Authorization': 'Bearer ' + token},
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_cart_get_valid(self, client):
        token = create_token()
        res = client.get('/carts/' + str(TestCartCrud.idcart),headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_cart_get_invalid_id(self, client):
        token = create_token()
        res = client.get('/carts/30',headers={'Authorization': 'Bearer ' + token},content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_cart_invalid_post_name(self, client):
        data = {'user_id': 5, 'status': 'gagal'}
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/carts/checkout',
                          data=json.dumps(data),
                          content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 500

    def test_barang_valid_put_token(self, client):
        token = create_token()
        data = {
            "user_id": 1 
        }
        res = client.delete('/carts/plusjumlah/' + str(TestCardCrud.idcart),
                        data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200


    def test_barang_valid_put_token(self, client):
        token = create_token()
        data = {
            "user_id": 1 
        }
        res = client.delete('/carts/plusjumlah/' + str(TestCartCrud.idcart),
                        data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_barang_valid_delete_token(self, client):
        token = create_token()
        data = {
            "user_id": 1 
        }
        res = client.delete('/carts/deletecart/' + str(TestBarangCrud.idcart),
                        data=json.dumps(data),
                         headers={'Authorization': 'Bearer ' + token},
                         content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_carts_invalid_delete(self, client):
        token = create_token()
        data = {
            "user_id": 1 
        }
        res = client.delete('/carts/deletecart/12',
                        data=json.dumps(data),
                         content_type='application/json',
        res_json = json.loads(res.data))
        assert res.status_code == 403

    def test_cart_valid_option(self, client):
        res = client.options('/carts/checkout')

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_cartdelete_valid_option(self, client):
        res = client.options('/carts/deletecart/'+str(TestCartCrud.idcart))

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
        
    def test_cartjumlah_valid_option(self, client):
        res = client.options('/carts/minusjumlah/'+str(TestCartCrud.idcart))

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
        
    def test_cartminus_valid_option(self, client):
        res = client.options('/carts/plusjumlah/'+str(TestCartCrud.idcart))

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
        
    def test_cartresource_valid_option(self, client):
        res = client.options('/carts/'+str(TestCartCrud.idcart))

        res_json = json.loads(res.data)
        assert res.status_code == 200


class TestTransaksiCrud ():
    idtransaksi = 0
    def test_transaksi_valid_option(self, client):
        res = client.options('/transaksi/status')

        res_json = json.loads(res.data)
        assert res.status_code == 200