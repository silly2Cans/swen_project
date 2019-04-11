# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

class Config(object):
    ##this is our  database at aws ec2
    ##SQLALCHEMY_DATABASE_URI = "mysql://swen_main_:mixednuts@swen-db.cakbys7wmjxf.eu-west-1.rds.amazonaws.com:3306/dublin_bikes"
    ##this is my local database info
    SQLALCHEMY_DATABASE_URI = "mysql://jeff:jeff003@localhost:3306/jack"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)


db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(debug=True)






