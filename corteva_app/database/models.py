from corteva_app.app import db
import sqlalchemy as sa


# We will subclass db.Model to create our individual data models. SQLAlchemy will use these models to create tables.
# However we will use SQLAlchemy directly for datatypes, since the db object does not properly namespace types.

class Weather(db.Model):
    # using a denormalized pattern for weather, meaning each station will have many measurements and will be repeated in this table
    id = db.Columns(sa.INT, primary_key=True, nullable=False)
    station_id = db.Column(sa.TEXT, nullable=False)
    date = db.Column(sa.DATE, nullable=False)
    max_temp = db.Column(sa.FLOAT, nullable=False)
    min_temp = db.Column(sa.FLOAT, nullable=False)
    precip = db.Column(sa.FLOAT, nullable=False)

class Yield(db.Model):
    # use year as primary key because it will be unique in this table. No need for an integer ID
    year = db.Column(sa.INT, primary_key=True, nullable=False)
    total_grain_yield = db.Column(sa.INT, nullable=False)

class WeatherStats(db.Model):
    year = db.Column(sa.INT, primary_key=True, nullable=False)
    station_id = db.Column(sa.TEXT, primary_key=True, nullable=False)
    # the combo of year/station_id will be unique, so we can use a multi-column primary key
    __table_args__ = (
        sa.PrimaryKeyConstraint(year, station_id),
        {},
    )
    avg_max_temp = db.Column(sa.FLOAT, nullable=False)
    avg_min_temp = db.Column(sa.FLOAT, nullable=False)
    total_precip = db.Column(sa.FLOAT, nullable=False)
