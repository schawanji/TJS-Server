import flask
from flask import Flask, render_template, request
import requests
import geopandas as gpd
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

CovidDataURL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/6a6a67340325c354e9ee4890816718391b47d9ac/us' \
               '-states.csv '
# FrameworkURI = "http://localhost:8080/geoserver/gwc/service/tms/1.0.0/topp%3Astates@EPSG%3A4326@geojson/0/0/0.geojson"

GetDataURL = "https://schawanji.herokuapp.com/static/covid_data.csv"

FrameworkKey = 'state'

FrameworkURI = 'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json'


'https://schawanji.herokuapp.com/tjs/api/joindata?FrameworkURI=https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json&GetDataURL=https://schawanji.herokuapp.com/static/covid_data.csv&FrameworkKey=state '



def get_framework_data(FrameworkURI):
    gdf = gpd.read_file(FrameworkURI)
    return gdf


def get_attribute_data(GetDataURL):
    df = pd.read_csv(GetDataURL)
    return df


def get_framework_key(FrameworkKey, attribute1, attribute2):
    FrameworkKey = str(FrameworkKey)
    attribute_1 = str(attribute1)
    attribute_2 = str(attribute2)
    return [FrameworkKey, attribute_1, attribute_2]


def attribute_csv(CovidDataURL):
    df = get_attribute_data(GetDataURL)

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    filtered_df = df.query("date >= '2020-01-21' \
                               and date < '2020-02-21'")
    df = df.query("date == '2021-01-29'")
    df = df[['state', 'deaths', 'cases']]
    df.to_csv(r'static\covid_data.csv', index=False, header=True)
    # Get url for a static file.
    with app.test_request_context():
        att_uri = flask.url_for("static", filename="covid_data.csv")
        print(att_uri)
    return df


def joindata(FrameworkURI, GetDataURL, FrameworkKey):
    # Joining operation.
    gdf = get_framework_data(FrameworkURI)
    df = get_attribute_data(GetDataURL)
    frameworkKey = gdf['name']
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


@app.route('/tjs/framework', methods=['GET'])
def get_framework():
    gdf = gpd.read_file(FrameworkURI)
    geojson = gdf.to_json()
    return geojson


@app.route('/tjs/api/joindata', methods=['GET'])
def join_data():
    # Input parameters required
    FrameworkURI = request.args.get('FrameworkURI')
    GetDataURL = request.args.get('GetDataURL')
    FrameworkKey = request.args.get('FrameworkKey')
    # Joining operation.
    gdf = get_framework_data(FrameworkURI)
    df = get_attribute_data(GetDataURL)
    frameworkKey = gdf['name']
    dataKey = str(FrameworkKey)
    df = df.rename(columns={dataKey: 'name'})
    df = df[['name', 'deaths', 'cases']]
    geometry = gdf[['geometry', 'name']]
    geometry = geometry.merge(df, on='name').reindex(gdf.index)
    geojson = geometry.to_json()
    return geojson


""""@app.route('/tjs/api', methods=['GET'])
def join_data():
    # Input parameters required
    FrameworkURI = request.args.get('FrameworkURI')
    GetDataURL = request.args.get('GetDataURL')
    FrameworkKey = request.args.get('FrameworkKey')
    attribute1 = request.args.get('attribute1')
    attribute2 = request.args.get('attribute2')
    # Joining operation.
    gdf = get_framework_data(FrameworkURI)
    adf = get_attribute_data(GetDataURL)
    keys = get_framework_key(FrameworkKey, attribute1, attribute2)
    gdf_columns = ['UN_A3', 'geometry']
    adf_columns = keys
    adf = adf.reindex(columns=adf_columns)
    gdf = gdf.reindex(columns=gdf_columns)
    adf['UN_A3'] = adf['UN_A3'].astype(int)
    gdf['UN_A3'] = gdf['UN_A3'].astype(int)
    geometry = gdf[['geometry', 'UN_A3']]
    attributes = adf[keys]
    geometry = geometry.merge(attributes, on='UN_A3').reindex(gdf.index)
    geojson = geometry.to_json()
    return geojson"""

if __name__ == "__main__":
    app.run()
