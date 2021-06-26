from flask import Flask, render_template, request
import requests
import geopandas as gpd
import pandas as pd

app = Flask(__name__)

vt_source = 'http://localhost:8080/geoserver/gwc/service/tms/1.0.0/topp%3Astates@EPSG%3A4326@geojson'

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


@app.route('/')
def index():
    title = "VectorTiles-Table Joining Service"
    return render_template("index.html", title=title)


@app.route('/tjs')
def api():
    title = "Table Joining Service API"
    return render_template("tjs.html", title=title)

@app.route('/tjs/attributes')
def attributes():
    title = "Table Joining Service API"
    return render_template("attributes.html", title=title)

@app.route('/tjs/frameworks', methods=['GET'])
def get_frameworks():
    geojson_vt = requests.get(vt_source)
    vt_source_metadata = [geojson_vt.url]
    if geojson_vt.status_code == 200:

        return render_template("frameworks.html", vt_source_metadata=vt_source_metadata)
    else:
        return 'Check if URL is correct'


@app.route('/tjs/api', methods=['GET'])
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
    return geojson


if __name__ == "__main__":
    app.run()
