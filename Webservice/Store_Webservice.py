import os
import flask
import pyodbc
import logging

import flask_restless
from flask_cors import CORS
import yaml

from Webservice.ConnectionString import ConnectionString
from Webservice.WebserviceResultBuilder import WebserviceResultBuilder

directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file_name = os.path.join(directory, 'conf', 'prod.yaml')
if not os.path.exists(config_file_name):
    config_file_name = os.path.join(directory, 'conf', 'dev.yaml')
with open(config_file_name, 'r') as ymlfile:
    config = yaml.load(ymlfile)

app = flask.Flask(__name__)
app.config['DEBUG'] = config['webservice']['debug']

logger = logging.getLogger(__name__)
logger.warning(' * demodata=' + str(config['webservice']['demodata']))

if config['webservice']['demodata']:
    # We're providing demodata from a PostgreSQL db through flask-restless
    from Webservice.DbModels import *

    app.config['SQLALCHEMY_DATABASE_URI'] = ConnectionString.from_config(config['demo_database'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

    # Create the database tables.
    db.create_all()

    # Create the Flask-Restless API manager.
    manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

    # Create API endpoints, which will be available at /api/<tablename> by
    # default. Allowed HTTP methods can be specified as well.
    manager.create_api(Board, results_per_page=0, methods=['GET', 'POST', 'PUT', 'DELETE'])


else:
    # We're providing real data by querying Lagerverwaltung database
    @app.route('/api/board', methods=['GET'])
    def get_boards():
        server = config['database']['ip_address'] + '\\' + config['database']['instance']
        connection = pyodbc.connect(driver=config['database']['driver'],
                                    server=server,
                                    uid=config['database']['user'],
                                    pwd=config['database']['password'])

        cursor = connection.execute('SELECT * FROM [lagerdb].[dbo].[GetBestand]() ORDER BY Material')

        results = WebserviceResultBuilder.get_results_with_description(cursor)
        cursor.close()
        connection.close()

        return WebserviceResultBuilder.build_json(results)

cors = CORS(app)

# start the flask loop
app.run(host=config['webservice']['host'], port=config['webservice']['port'])
