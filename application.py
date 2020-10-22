from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initiate application
application = Flask(__name__)

# Database
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:msci436project@uni-dss.cmuqyhsxn149.us-east-2.rds.amazonaws.com:3306/uni_dss'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # To prevent any complaints in console

# Initialize DB
db = SQLAlchemy(application)

# Initialize marshmallow
ma = Marshmallow(application)

# Classes, constructors, schemas & initiate

@application.route('/create-user', methods=['POST'])
def create_user():
    # Actions
    return 3

# Run server
if __name__ = '__main__':
    application.run(host='0.0.0.0')