import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/food.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
food_db = Base.classes.Food_file

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/data")
def names():
    """Return all data."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(food_db).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    data = df.to_json(orient='records')

    # return data in json objects
    return data

if __name__ == "__main__":
    app.run()
