from corteva_app.app import db
import sqlalchemy as sa


# We will subclass db.Model to create our individual data models. SQLAlchemy will use these models to create tables.
# However we will use SQLAlchemy directly for datatypes, since the db object does not properly namespace types and I love my VSCode autocompletes.

class Weather(db.Model):
    # using a denormalized pattern for weather, meaning each station will have many measurements and will be repeated in this table
    # use station_id/date combo for primary key for easy de-duping
    station_id = db.Column(sa.TEXT, primary_key=True, nullable=False)
    date = db.Column(sa.DATE, primary_key=True, nullable=False)
    __table_args__ = (
        sa.PrimaryKeyConstraint(station_id, date),
        {},
    )
    max_temp = db.Column(sa.FLOAT, nullable=True, comment="maximum temperature in degrees C")
    min_temp = db.Column(sa.FLOAT, nullable=True, comment="minimum temperature in degrees C")
    precip = db.Column(sa.FLOAT, nullable=True, comment="precipitation in centimeters")

class Yield(db.Model):
    # use year as primary key because it will be unique in this table
    year = db.Column(sa.INT, primary_key=True, nullable=False)
    total_grain_yield = db.Column(sa.INT, nullable=False, comment="total harvested corn grain yield in 1000s of megatons")

class WeatherStats(db.Model):
    station_id = db.Column(sa.TEXT, primary_key=True, nullable=False)
    year = db.Column(sa.INT, primary_key=True, nullable=False)
    # the combo of station_id/year will be unique, use as primary key for easy de-duping
    __table_args__ = (
        sa.PrimaryKeyConstraint(station_id, year),
        {},
    )
    avg_max_temp = db.Column(sa.FLOAT, nullable=True, comment="average maximum temperature in degrees C")
    avg_min_temp = db.Column(sa.FLOAT, nullable=True, comment="average minimum temperature in degrees C")
    total_precip = db.Column(sa.FLOAT, nullable=True, comment="total accumulated precipitation in centimeters")
