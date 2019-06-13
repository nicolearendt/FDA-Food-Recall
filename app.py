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
def allData():
    """Return all data."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(food_db).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    data = df.to_json(orient='records')
    # return data in json objects
    return data

@app.route("/data/<start_date>/<end_date>")
def start_end(start_date, end_date):
    """Return filtered data between start and end date."""
    #dates appear in the format : 2012-08-01
    start_date = start_date.replace("-","/")
    end_date = end_date.replace("-","/")

    print(end_date)

    if len(end_date) < 10:
        end_date = end_date + "/31"

    print(end_date)

    # Use Pandas to perform the sql query
    start_end_recalls = db.session.query(food_db).\
        filter(food_db.recall_date >= start_date).\
        filter(food_db.recall_date <= end_date).group_by(food_db.recall_date).statement
    

    df = pd.read_sql_query(start_end_recalls, db.session.bind)
    recalls_list = df.to_json(orient='records')
    
    return recalls_list

@app.route("/data/<classification>/<start_date>/<end_date>")
def class_start_end(start_date, end_date, classification):
    """Return filtered data between start and end date and filter by class."""
    #dates appear in the format : 2012-08-01
    start_date = start_date.replace("-","/")
    end_date = end_date.replace("-","/")

    print(end_date)

    if len(end_date) < 10:
        end_date = end_date + "/31"

    print(end_date)

    #classification appears in this format : Class I

    # Use Pandas to perform the sql query
    start_end_class_recalls = db.session.query(food_db).\
        filter(food_db.recall_date >= start_date).\
        filter(food_db.recall_date <= end_date).\
        filter(food_db.classification == classification).group_by(food_db.recall_date).statement
    

    df = pd.read_sql_query(start_end_class_recalls, db.session.bind)
    recalls_class_list = df.to_json(orient='records')
    
    return recalls_class_list

if __name__ == "__main__":
    app.run()
