# run this to populate the database with tables as defined in our data models

from corteva_app.app import app, db
# need to import the models or else the db object doesn't know what tables to create
from corteva_app.database import models

with app.app_context():
    db.create_all()