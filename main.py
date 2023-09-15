import flask
from flask import Flask, render_template, request, redirect, url_for
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

GetDataURL = "https://schawanji.herokuapp.com/static/covid_data.csv"
FrameworkKey = 'name'
AttributeKey = 'state'
FrameworkURI = 'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json'

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
        gdf = gpd.read_file(r.text)
        gdf = gdf[['geometry', FrameworkKey]]
        geojson = gdf.to_json()
        return geojson


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


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    app.run()
