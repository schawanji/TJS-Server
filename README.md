# TJS-Server
TJS-Server contain a web API that facilitate data joining operation based on OCG Table Joining Service TJS.

# What is TJS?

TJS is an OGC standard interface for joining tabular data to a geospatial framework. TJS-Server contain an API that takes in tabular data in CSV format and intergrate it with a vector tiles in GeoJSON format.

# Manual installation of TJS-Server

Python 3x

Python packages (See also requirements.txt):
Flask
GeoPandas 
Pandas 

# Supported operation:
joindata service

# Using joindata service
The service must be called with 5 parameters http GET request:
vtc_url 
attribute_url
framework_key
attribute1
attribute2

# Example:
The url below accesses vector tiles that can be rendered in a GIS application that supports vector tiles in GeoJSON format.

http://127.0.0.1:5000/tjs/api?vtc_url=[url]&attribute_url=[url]&framework_key=[key]&attribute1=[column_name]&attribute2=[column_name]

vtc_url points to a vector tile URL.vtc_url should take the form:

http://localhost:8080/geoserver/gwc/tms/1.0.0/layername@grisetId@formatExtension/z/x/y.format

z is zoom level
x and y define a given tile coordinates
gridsetId refers to the coordinate reference system
format refers to format of the vector tiles 


attribute_url points to a CSV file URL. attribute_url takes the form:

http://127.0.0.1:8000/sample-csv.csv

framework_key, attribute1 and attribute2 are names of CSV columns.






