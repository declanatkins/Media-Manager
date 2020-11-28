import connexion
from flask_cors import CORS


APP = connexion.FlaskApp(__name__)
APP.add_api('swagger.yaml')

CORS(APP.app)