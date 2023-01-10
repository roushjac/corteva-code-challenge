from corteva_app.app import db

# We will subclass db.Model to create our individual data models

class Weather(db.Model):
    pass

class Yield(db.Model):
    pass

class WeatherStats(db.Model):
    pass