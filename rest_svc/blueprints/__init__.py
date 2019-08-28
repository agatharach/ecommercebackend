from  flask import Flask,request
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['APP_DEBUG'] = True
# JWT
app.config['JWT_SECRET_KEY']='VS-REjgGDMq3Ne2AMhjK'
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(days=30)

# database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:Altabatch3@ecommerce.cwpvjetmrbmv.ap-southeast-1.rds.amazonaws.com/eCommerce"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# jwt
jwt = JWTManager(app)

def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if (int(claims['status']) == 1 ):
            return fn(*args, **kwargs)
        else :
            return {'status':'FORBIDDEN', 'message' : 'Users Only'},403         
    return wrapper

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.after_request
def after_request(response):
    try :
        requestData = request.get_json()
    except :
        requestData = request.args.to_dict()
    
    app.logger.warning("REQUEST_LOG\t%s",
        json.dumps({
            'method' : request.method,
            'code' : response.status,
            'url' : request.full_path,
            'request' : requestData,
            'response' : json.loads(response.data.decode('utf-8'))
        })
        )
    return response

from blueprints.user.resources import bp_user
app.register_blueprint(bp_user, url_prefix='/users')
from blueprints.cart.resources import bp_cart
app.register_blueprint(bp_cart, url_prefix='/carts')
from blueprints.barang.resources import bp_barang
app.register_blueprint(bp_barang, url_prefix='/items')
from blueprints.transaksi.resources import bp_transaksi
app.register_blueprint(bp_transaksi, url_prefix='/transaksi')

db.create_all()