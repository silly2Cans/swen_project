# coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


class Config(object):
    
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/db_python04"

 
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)


db = SQLAlchemy(app)


if __name__ == '__main__':
    
    

    db.create_all()







