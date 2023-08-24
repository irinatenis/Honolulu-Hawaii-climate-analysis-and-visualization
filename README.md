# Honolulu, Hawaii, climate analysis and visualization
## **Goal**:
To do a climate analysis of Honolulu, Hawaii, and design a climate app
## **Data**:
SQLite file and 2 csv files with measurements and stations names*
## **Tools**: 
Python (Pandas, NumPy, datetime, and Matplotlib), SQLAlchemy, Flask
### **Climate Data Analysis**:
1. Used SQLAlchemy to connect to the SQLite database and reflected tables into classes 
2. Linked Python to the database by creating a SQLAlchemy session and ran the queries for precipitation and stations data
3. Saved the query results to Pandas DataFrames and plotted them
### **Climate App Design**:
1. Used Flask to create a homepage that lists 5 avalable routes, both static and dynamic
2. Applied the queries from the previous part to return JSON lists of observations/calculations for each route

#### *References
Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xmlLinks to an external site.
