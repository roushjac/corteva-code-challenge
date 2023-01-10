# run this to populate the database with tables as defined in our data models

from corteva_app.app import app, db
from corteva_app.database import models

with app.app_context():
    db.create_all()