#!/usr/bin/python3
from gender_project.model import *
from gender_project.database_requests import *

from flask import Flask
from flask import jsonify


# SQLAlchemy
# Use following credentials:
# hostname: relational.fit.cvut.cz
# port: 3306
# username: guest
# password: relational

# engine = create_engine("mysql://flask_user:password@localhost/ftp", echo=False)
engine = create_engine("mysql://guest:relational@relational.fit.cvut.cz:3306/ftp", echo=False)
connection = engine.connect()
# create a configured "Session" class
Session = sessionmaker(bind=engine)
# create a Session
session = Session()

#load predictive model
PATH_TO_DATA = './models/'
with open(os.path.join(PATH_TO_DATA, 'A.pkl'), mode = 'rb') as file:
    production_model = pickle.load(file)


# flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/count/<string:session_id>/<string:category>', methods=['GET'])
def get_count(session_id, category):
    return jsonify(get_response_on_category_in_session(session_id,
                                                       category,
                                                       session))


@app.route('/predict/<string:session_id>', methods=['GET'])
def get_prediction(session_id):
    return jsonify(get_prediction_response(session_id, session, production_model))


if __name__ == '__main__':
    app.run()
