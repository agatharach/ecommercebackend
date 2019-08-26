from blueprints import db
from flask_restful import fields

class Trx(db.Model):
    __tablename__="transaksi"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    barang_id = db.Column(db.Integer, db.ForeignKey('barang.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(25))
    alamat = db.Column(db.String(50), nullable=False)
    nomorhp = db.Column(db.String(20),nullable=False)
    status = db.Column(db.String(25),nullable=False)
    totalharga = db.Column(db.Integer,nullable=False)
    metodebayar = db.Column(db.String(50), nullable=False)
    kurir = db.Column(db.String(25),nullable=False)

    response_fields = {
        'id' : fields.Integer,
        'barang_id' : fields.Integer,
        'user_id' : fields.Integer,
        'jumlah' : fields.Integer,
        'username' : fields.String,
        'alamat' : fields.String,
        'nomorhp' : fields.String,
        'status' : fields.String,
        'totalharga' : fields.Integer,
        'metodebayar' : fields.String,
        'kurir' : fields.String, 
    }

    response_fields_summary = {
        'id' : fields.Integer,
        'barang_id' : fields.Integer,
        'user_id' : fields.Integer,
        'jumlah' : fields.Integer,
        'totalharga' : fields.Integer,
    }

    def __init__(self,barang_id,customer_id,jumlah,nama,alamat,nomorhp,status,totalharga,metodebayar,kurir):
        self.barang_id = barang_id
        self.user_id = customer_id
        self.jumlah = jumlah
        self.username = nama
        self.alamat = alamat
        self.nomorhp = nomorhp
        self.status = status
        self.totalharga = totalharga
        self.metodebayar = metodebayar
        self.kurir = kurir


    def __repr__(self):
        return '<Trx %r>'% self.id