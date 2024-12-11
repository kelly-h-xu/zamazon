from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect() 
from flask_cors import CORS 
login = LoginManager()
login.login_view = 'users.login'


def create_app():
    # initialize flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    csrf.init_app(app) 
    CORS(app, origins="http://localhost:3000", supports_credentials=True)
    
    # initialize the db on login
    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    # users routes
    from .users import bp as user_bp
    app.register_blueprint(user_bp)
    from .account import bp as account_bp
    app.register_blueprint(account_bp)
    from .purchase_history import bp as purchase_hist_bp
    app.register_blueprint(purchase_hist_bp)
    
    # social related routes
    from .social import bp as social_bp
    app.register_blueprint(social_bp)

    # products related routes
    from .products import bp as product_bp
    app.register_blueprint(product_bp)
    
    # cart related routes
    from .cartView import bp as carts_bp
    app.register_blueprint(carts_bp)

    from .sellers import bp as seller_bp
    app.register_blueprint(seller_bp)

    return app
