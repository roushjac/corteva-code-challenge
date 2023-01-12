# Corteva Code Challenge

## Step 1 - Python virtual environment and database creation

These instructions assume you are using a Linux based distro such as Ubuntu, however the Python specific commands will also work on Windows/MacOS.

Run the following command to create a virtual environment. Virtual environments are essential for package and dependency management on local and cloud systems.

`python3 -m venv .venv`

```
source .venv/bin/activate
pip install -r requirements.txt
```

We will be running the PostgreSQL service on our local machine.

```
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```

Before we can create our database we need to set up at least one user with a password. For simplicity we will use the default admin user called `postgres`. However, it does need a password to be set before we can use it.

Enter this command:

`sudo passwd postgres`

And paste this (very creative) password in the prompt.

`password`

Now we can create the database and use SQLAlchemy to create the tables using our data models. Run this to create a new database with the admin user.

`sudo -u postgres createdb corteva-db`

Finally, we can run a small Python program to populate the database with tables following our data models.

```
cd utils
python create_db_tables.py
```

To confirm that we have set this up correctly:

1. `sudo -u postgres psql` to activate the postgres service
2. `\c corteva-db` to connect to the proper database
3. `\dt` should list 3 tables
4. `\q` to quit out of the postgres command line

## Step 2 - Ingest data

This one is made simple for the user with the help of a utility script. It will populate the weather and yield tables using the provided flat files and SQLAlchemy data models defined in our app.

`cd utils` if not already in the `corteva-code-challenge/utils` directory.

`python ingest_data.py`

We can view the data using a database viewer program such as DBeaver or PGAdmin, or directly from the psql command line.

## Step 3 - Analysis

In the `utils` directory we can run `python calculate_stats.py` to execute a SQL statement that will run the analysis and populate the `weather_stats` table.
This executes raw SQL and does not use the ORM features of SQLAlchemy. The query is just too complex to justify writing it in ORM form.

Since we are aggregating at the year level, we cannot include records from the `weather` table that do not have continuous data. Including this incomplete data would skew our summary statistics and could lead us to incorrect conclusions.

If we wanted to include more data, we could set a criteria for how many missing days we are willing to accept. In this analysis I did not accept years missing 1 or more days of data. We could also aggregate at the seasonal or month level if we are interested in exploring seasonal trends.

## Step 4 - Deliver data through Flask REST API

Navigate to the directory containing the Flask app.

`cd corteva_app`

You must be in the `corteva-code-challenge/corteva_app` directory to run the app.

Run this command to bring the API online:

`flask run`

At this point, all tables have been created according to our models, data has been ingested, and a local server is able to deliver this data. Open up a new shell and run these example commands one at a time to confirm everything is working as expected.

```
curl "localhost:5000/api/weather/stats?station_id=USC00110072"
curl "localhost:5000/api/weather/stats?year=2000&station_id=USC00110072"

curl "localhost:5000/api/weather?date=1985-01-01"
curl "localhost:5000/api/weather?station_id=USC00137161"

curl "localhost:5000/api/yield"
curl "localhost:5000/api/yield?year=2013"
```