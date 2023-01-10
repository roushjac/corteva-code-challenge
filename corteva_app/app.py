from flask import Flask
from corteva_app.database import db_session

# initialize the main Flask object with the special dunder variable __name__
# we will use this to define API routes
app = Flask(__name__)

# this should close open database connections when requests complete or the app shuts down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()