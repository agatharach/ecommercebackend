from blueprints import db
from flask_restful import fields

class Users(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    alamat = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Integer) 
    nomorhp = db.Column(db.String(25),nullable=False)

    response_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'alamat' : fields.String,
        'status' : fields.Integer,
        'nomorhp' : fields.String,
    }

    def __init__(self,username,password,alamat,status,nomorhp):
        self.username = username
        self.password = password
        self.alamat = alamat
        self.status = status
        self.nomorhp = nomorhp

    def __repr__(self):
        return '<User %r>'% self.id