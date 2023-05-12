# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os 
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
#Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect an existing database into a new model
Base = automap_base()

#Reflect the tables
Base.prepare(autoload_with=engine)

#Save references to each table
Measurement = Base.classes.measurement
Station=Base.classes.station

#Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# FLASK SETUP
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
   
    # """List all available api routes."""
    return (
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end>"
    ) 

# PRECIPITATION: Convert the query results from precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of the dictionary.     
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return last year precipitation analysis"""
    # Query last year precipitation
    results = session.query(Measurement.prcp, Measurement.date).\
    filter(Measurement.date<= dt.date(2017,8,23),Measurement.date>=dt.date(2016, 8, 23)).order_by(Measurement.date).all()
    session.close()
    # Create a JSON list of results
    last_year_precipitation = []
    for prcp,date in results:
        precipitation_dict = {}
        precipitation_dict[date]=prcp
        last_year_precipitation.append(precipitation_dict)
    return jsonify(last_year_precipitation)

# STATIONS:  Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list and jsonify it
    station_names = list(np.ravel(results))
    return jsonify(station_names)
    
# OBSERVATIONS FOR MOST ACTIVE STATION: Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def active_station_observations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return temperature observations for the previous year."""
    # Query the last 12 months of temperature observation data for the most active station
    results=session.query(Measurement.tobs, Measurement.date).\
    filter(Measurement.date<= dt.date(2017,8,23),Measurement.date>=dt.date(2016, 8, 23)).\
    filter(Measurement.station == 'USC00519281').\
    all()
    # Create a JSON list of observations
    observations = []
    for tobs, date in results:
        observations.append(tobs)
    return jsonify(observations)

#START DATE: Calculate  and return a JSON list of TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
@app.route("/api/v1.0/<start>")

def start_date(start):
    # Set start date
    startDate=(start)
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    results=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date>=startDate).all()
    session.close()
    # Create a JSON list of the calculations
    TMIN_TAVG_TMAX = []
    for min, max, avg in results:
        stats={}
        stats["min"]=min
        stats['max']=max
        stats['avg']=avg
        TMIN_TAVG_TMAX.append(stats)
    return jsonify(TMIN_TAVG_TMAX)

# START AND END DATE: For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end>")

def start_end_date(start,end):
    # Set start and end dates for date range
    startDate=(start)
    endDate=(end)
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    results=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date>=startDate, Measurement.date<=endDate).all()
    session.close()
    # Create a JSON list of the calculations
    TMIN_TAVG_TMAX = []
    for min, max, avg in results:
        stats={}
        stats["min"]=min
        stats['max']=max
        stats['avg']=avg
        TMIN_TAVG_TMAX.append(stats)
    return jsonify(TMIN_TAVG_TMAX)

if __name__ == "__main__":
    app.run(debug=True)