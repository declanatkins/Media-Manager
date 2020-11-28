from setuptools import setup
from setuptools import find_packages


setup(
    name='Media API',
    version='0.0.1',
    description='An API for managing Media',
    author='Declan Atkins',
    author_email='declanatkins@gmail.com',
    packages=find_packages(),
    package_data={
      '': ['swagger.yaml']  
    },
    include_package_data=True,
    install_requires=[
        'connexion[swagger-ui]==2.7.0',
        'gunicorn==20.0.4',
        'pymongo==3.11.1',
        'flask-cors==3.0.9'
    ]
)