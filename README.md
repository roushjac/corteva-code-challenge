# Code Challenge Template

## Step 1 - Python virtual environment and database creation

These instructions assume you are using a Linux based distro such as Ubuntu, however the Python specific commands will also work on Windows/MacOS.

Run the following command to create a virtual environment. Virtual environments are essential for package and dependency management on local or cloud systems.
`python3 -m venv .venv`

Run these commands to activate the virtual environment and install the packages needed to create and manage the database. It will also install Flask which we will use to deliver data later.
`source .venv/bin/activate`
`pip install -r requirements.txt`
