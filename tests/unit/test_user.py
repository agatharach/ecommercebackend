from app.users.model import Users as UserModel
from app import db
from mock import patch
from tests import reset_database

class TestUser():

    reset_database()

    def test_is_user_already_exist(self):

        datas = [
            {
                "username": "alterrans1",
                "password": "test",
                "phonenumber": "094653438",
                "address": "Malang"
            },
            {
                "username": "alterrans2",
                "password": "test",
                "phonenumber": "097563782",
                "address": "Jakarta"
            }
        ]

        # insert data
        for data in datas:
            user = UserModel(data['username'], data['password'], data['phonenumber'], data['address'])
            db.session.add(user)
            db.session.commit()

        username = "alterrans1"

        assert UserModel.is_exists(username) == True


    @patch.object(UserModel, 'is_exists')
    def test_if_get_last_balance_is_none(self, mock_is_exists):

        username = "alterrans2"
        mock_is_exists.return_value = True

        assert UserModel.is_exists(username) == True