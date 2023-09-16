import flask
from flask import Flask, render_template, request, redirect, url_for,jsonify
import requests
import geopandas as gpd
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def get_framework_data(FrameworkURI):
    gdf = gpd.read_file(FrameworkURI)
    gdf = gdf[['geometry', 'name']]
    return gdf


def get_attribute_data(GetDataURL):
    df = pd.read_csv(GetDataURL)
    return df


def get_framework_key(FrameworkKey, attribute1, attribute2):
    FrameworkKey = str(FrameworkKey)
    attribute_1 = str(attribute1)
    attribute_2 = str(attribute2)
    return [FrameworkKey, attribute_1, attribute_2]



#GetDataURL = "http://127.0.0.1:8000/static/covid_data.csv"
#FrameworkKey = 'name'
#AttributeKey = 'state'
#FrameworkURI = 'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json'


@app.route('/')
def index():
    title = "VectorTiles-Table Joining Service"
    return render_template("index.html", title=title)


@app.route('/form')
def form():
    title = "GET Framework"
    return render_template("form.html", title=title)


@app.route('/tjs/get_framework', methods=['POST', 'GET'])
def get_framework():
    if request.method == 'POST':
        FrameworkKey = request.form['frameworkkey']
        FrameworkURI = request.form['getframework']
        r = requests.get(FrameworkURI)
        print(r)
        gdf = gpd.read_file(r.text)
        gdf = gdf[['geometry', FrameworkKey]]
        geojson = gdf.to_json()
        return geojson
    else:
        return "This endpoint only accepts POST requests."

#curl -X POST -d "frameworkkey=SOVEREIGNT&getframework=https://raw.githubusercontent.com/martynafford/natural-earth-geojson/master/10m/cultural/ne_10m_admin_0_countries.json" http://127.0.0.1:8000/tjs/get_framework
#curl -X POST -d "frameworkkey=SOVEREIGNT&getframework=https://raw.githubusercontent.com/martynafford/natural-earth-geojson/master/10m/cultural/ne_10m_admin_0_countries.json" https://schawanji-tjs-server-demo.up.railway.app/tjs/get_framework



@app.route('/tjs/api/getjoindata', methods=['GET'])
def getjoindata():
    # Input parameters required
    FrameworkURI = request.args.get('FrameworkURI')
    GetDataURL = request.args.get('GetDataURL')
    FrameworkKey = request.args.get('FrameworkKey')
    AttributeKey = request.args.get('AttributeKey')
    gdf = get_framework_data(FrameworkURI)
    df = get_attribute_data(GetDataURL)
    dataKey = str(FrameworkKey)
    df = df.rename(columns={dataKey: 'name'})
    df = df[['name', 'deaths', 'cases']]
    geometry = gdf[['geometry', 'name']]
    geometry = geometry.merge(df, on='name').reindex(gdf.index)
    geojson = geometry.to_json()
    return geojson


@app.route('/tjs/api/joindata', methods=['GET'])
def tjsapi_joindata():
    # Input parameters required
    FrameworkURI = request.args.get('FrameworkURI')
    GetDataURL = request.args.get('GetDataURL')
    FrameworkKey = request.args.get('FrameworkKey')
    AttributeKey = request.args.get('AttributeKey')
    # Joining operation.
    gdf = get_framework_data(FrameworkURI)
    df = get_attribute_data(GetDataURL)
    dataKey = AttributeKey
    df = df.rename(columns={dataKey: FrameworkKey})
    geometry = gdf[['geometry', FrameworkKey]]
    geometry = geometry.merge(df, on=FrameworkKey).reindex(gdf.index)
    geojson = geometry.to_json()
    return geojson
    
#http://127.0.0.1:8000/tjs/api/joindata?FrameworkURI=https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json&GetDataURL=https://schawanji-tjs-server-demo.up.railway.app/static/covid_data.csv&FrameworkKey=name&AttributeKey=state
#http://127.0.0.1:8000/tjs/api/getjoindata?FrameworkURI=https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json&GetDataURL=https://schawanji-tjs-server-demo.up.railway.app/static/covid_data.csv&FrameworkKey=name

@app.route('/join_data', methods=['GET'])
def join_data():
    # Get query parameters from the request
    FrameworkURI = request.args.get('FrameworkURI')
    GetDataURL = request.args.get('GetDataURL')
    FrameworkKey = request.args.get('FrameworkKey')
    AttributeKey = request.args.get('AttributeKey')

    # Replace this code with your actual data retrieval and joining logic
    gdf = get_framework_data(FrameworkURI)  # Replace with your data retrieval function
    df = get_attribute_data(GetDataURL)      # Replace with your data retrieval function

    # Rename the DataFrame columns
    dataKey = AttributeKey
    df = df.rename(columns={dataKey: FrameworkKey})

    # Perform the join operation
    geometry = gdf[['geometry', FrameworkKey]]
    geometry = geometry.merge(df, on=FrameworkKey).reindex(gdf.index)

    # Convert the result to GeoJSON
    geojson = geometry.to_json()

    return jsonify(geojson)
#http://127.0.0.1:8000/join_data?FrameworkURI=https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json&GetDataURL=http://127.0.0.1:8000/static/covid_data.csv&FrameworkKey=name&AttributeKey=state
#https://schawanji-tjs-server-demo.up.railway.app/join_data?FrameworkURI=https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json&GetDataURL=https://schawanji-tjs-server-demo.up.railway.app/static/covid_data.csv&FrameworkKey=name&AttributeKey=state
#http://127.0.0.1:8000/get_geojson?FrameworkURI=https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json
###################


@app.route('/get_geojson', methods=['GET'])
def get_geojson():
    try:
        # Get the 'url' parameter from the request's query string
        FrameworkURI = request.args.get('FrameworkURI')
        
        if  FrameworkURI:
            # Fetch the GeoJSON data from the specified URL
            response = requests.get( FrameworkURI)
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Set the content type to GeoJSON
                response.headers['Content-Type'] = 'application/json'
                # Return the GeoJSON data as a response
                return response.text
            else:
                return jsonify({"error": "Failed to fetch GeoJSON data"}), 500
        else:
            return jsonify({"error": "URL parameter 'url' is missing"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 50


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
