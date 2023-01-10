from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from corteva_app.database import db_session, conn_str

# create Flask's SQLAlchemy extension object
db = SQLAlchemy()

# initialize the main Flask object with the special dunder variable __name__
# we will use this to define API routes and set app configs
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = conn_str

# initialize the app with the extension
db.init_app(app)

# this should close open database connections when requests complete or the app shuts down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()