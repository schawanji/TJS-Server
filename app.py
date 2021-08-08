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


def joindata(FrameworkURI, GetDataURL, FrameworkKey):
    # Joining operation.
    gdf = get_framework_data(FrameworkURI)
    df = get_attribute_data(GetDataURL)
    dataKey = str(FrameworkKey)
    df = df.rename(columns={dataKey: 'name'})
    df = df[['name', 'deaths', 'cases']]
    geometry = gdf[['geometry', 'name']]
    geometry = geometry.merge(df, on='name').reindex(gdf.index)
    geojson = geometry.to_json()
    return geojson


@app.route('/')
def index():
    title = "VectorTiles-Table Joining Service"
    return render_template("index.html", title=title)


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


@app.route('/tjs/api/joindata', methods=['GET'])
def join_data():
    # Input parameters required
    FrameworkURI = request.args.get('FrameworkURI')
    GetDataURL = request.args.get('GetDataURL')
    FrameworkKey = request.args.get('FrameworkKey')
    gdf = get_framework_data(FrameworkURI)
    df = get_attribute_data(GetDataURL)
    dataKey = str(FrameworkKey)
    df = df.rename(columns={dataKey: 'name'})
    df = df[['name', 'deaths', 'cases']]
    geometry = gdf[['geometry', 'name']]
    geometry = geometry.merge(df, on='name').reindex(gdf.index)
    geojson = geometry.to_json()
    return geojson


if __name__ == "__main__":
    app.run()
