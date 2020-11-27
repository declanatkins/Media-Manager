import connexion


APP = connexion.FlaskApp(__name__)
APP.add_api('swagger.yaml')