from blueprints import db
from flask_restful import fields

class Carts(db.Model):
    __tablename__="cart"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    barang_id = db.Column(db.Integer, db.ForeignKey('barang.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    
    response_fields = {
        'id' : fields.Integer,
        'barang_id' : fields.Integer,
        'user_id' : fields.Integer,
        'jumlah' : fields.Integer,
    }

    def __init__(self,barang_id,user_id,jumlah):
        self.barang_id = barang_id
        self.user_id = user_id
        self.jumlah = jumlah
