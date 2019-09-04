from blueprints import db
from flask_restful import fields

class Barangs(db.Model):
    __tablename__="barang"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(75), nullable=False)    
    name = db.Column(db.String(75), nullable=False)
    stok = db.Column(db.String(25), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(25), nullable=False)
    urlfoto = db.Column(db.String(250))
    deskripsi = db.Column(db.String(250), nullable=False)    

    response_fields = {
        'id' : fields.Integer,
        'user_id' : fields.Integer,
        'username' : fields.String,
        'name' : fields.String,
        'stok' : fields.String,
        'harga' : fields.Integer,
        'category' : fields.String,
        'urlfoto' : fields.String,
        'deskripsi' : fields.String
    }

    def __init__(self,user_id,username,name,stok,harga,category,urlfoto,deskripsi):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.stok = stok
        self.harga = harga
        self.category = category
        self.urlfoto = urlfoto
        self.deskripsi = deskripsi
