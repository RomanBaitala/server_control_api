import os
from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from dotenv import load_dotenv

from flasgger import Swagger

from app.config.ext import db

from app.schemas.metric_schema import MetricCreate, MetricResponse
from app.utils.mqtt_bridge import start_mqtt_listener

from app.route.user_route import user_bp
from app.route.server_route import server_bp
from app.route.metric_route import metric_bp

from app.models import User, Server
from app.schemas import UserCreate, UserLogin, ServerCreate, ServerResponse, ServerUpdate, MetricCreate, MetricResponse

load_dotenv()


def init_mysql_database(db_url):
    url = make_url(db_url)
    
    base_url = f"mysql+pymysql://{url.username}:{url.password}@{url.host}:{url.port or 3306}"
    engine = create_engine(base_url)
    
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {url.database}"))
        
    print(f"База даних '{url.database}' готова.")

def create_app():
    app = Flask(__name__)
    
    template = {
        "swagger": "2.0",
        "info": {
            "title": "Server Control API",
            "version": "1.0"
        },
        "definitions": {
            "UserCreate": UserCreate.model_json_schema(),
            "UserLogin": UserLogin.model_json_schema(),
            "ServerCreate": ServerCreate.model_json_schema(),
            "ServerUpdate": ServerUpdate.model_json_schema(),
            "ServerResponse": ServerResponse.model_json_schema(),
            "MetricResponse": MetricResponse.model_json_schema(),
            "MetricCreate": MetricCreate.model_json_schema(),
        }
    }

    swagger = Swagger(template=template)

    db_url = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_mysql_database(db_url)

    db.init_app(app)

    swagger.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(server_bp)
    app.register_blueprint(metric_bp)

    with app.app_context():
        db.create_all()
        start_mqtt_listener(app)
        print("Таблиці бази даних синхронізовано.")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)