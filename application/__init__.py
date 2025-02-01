from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="env/db_config.env")
bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                template_folder=r'C:\Users\Jonna\OneDrive\Documentos\Estudos\Python\Social\templates',
                static_folder=r'C:\Users\Jonna\OneDrive\Documentos\Estudos\Python\Social\static')
    
   
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    bcrypt.init_app(app)


    from routes.login import loginView
    from routes.home import homeView
    from routes.action import actionView
    app.register_blueprint(homeView, url_prefix='/')
    app.register_blueprint(loginView, url_prefix='/')
    app.register_blueprint(actionView)

    

    return app