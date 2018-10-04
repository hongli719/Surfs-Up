import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def main():
    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"        
    )

@app.route("/api/v1.0/precipitation")
def prcp():

    # Calculate the date 2 year ago from today
    query_date = dt.date.today() - dt.timedelta(days = 730)

    # Perform a query to retrieve the data and precipitation scores
    result = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > query_date).order_by(Measurement.date.desc()).all()

    tobs = []

    for x in result:
        tobs_dict = {}
        tobs_dict[f"{x.date}"] = x.tobs
        tobs.append(tobs_dict)

    return jsonify(tobs)

@app.route("/api/v1.0/stations")
def station():

    # result1 = session.query(Station.station).all()

    # stations = []

    # for x in result1:
    #     stations.append(x)

    return jsonify(session.query(Station.station).all())

@app.route("/api/v1.0/tobs")
def tobs():

    query_date = dt.date.today() - dt.timedelta(days = 730)

    return jsonify(session.query(Measurement.tobs).filter(Measurement.date > query_date).all())

if __name__ == '__main__':
    app.run(debug=True)