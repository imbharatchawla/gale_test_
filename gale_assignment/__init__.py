from flask import Flask, json, request
from flask_restful import Resource, Api, reqparse
import config
import psycopg2
app = Flask(__name__, template_folder = '/home/guddu/gale/gale_assignment/templates')
api = Api(app)
app.config.from_object('config')
# pg_conn = psycopg2.connect(database=app.config['DB_NAME'], 
#                 user=app.config['DB_USER'], 
#                 password=app.config['PASSWORD'], host=app.config['HOST'])
pg_conn = psycopg2.connect(database="galetest",
                            user="galetest",
                            password="bharat",
                            host="localhost",
                            port="5432")
pg_conn.autocommit=True
#import routes in the end to avoid circular import errors as well
import gale_assignment.routes.routes