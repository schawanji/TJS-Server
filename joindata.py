import geopandas as gpd
import pandas as pd
from flask import Flask, request


app = Flask(__name__)


def get_frameworkdata(vtc_url):
    gdf = gpd.read_file(vtc_url)
    return gdf


def get_attributedata(attribute_url):
    df = pd.read_csv(attribute_url)
    return df


def get_frameworkkey(framework_key, attribute1, attribute2):
    framework_key = str(framework_key)
    attribute_1 = str(attribute1)
    attribute_2 = str(attribute2)
    return [framework_key, attribute_1, attribute_2]

@app.route('/')
def index():
    return '<!DOCTYPE html><html><head><title>Page Title</title></head><body><h1>This is a Heading</h1><p>This is a ' \
           'paragraph.</p></body></html> '


@app.route('/tjs/api', methods=['GET'])
def join_data():
    vtc_url = request.args.get('vtc_url')
    attribute_url = request.args.get('attribute_url')
    framework_key = request.args.get('framework_key')
    attribute1 = request.args.get('attribute1')
    attribute2 = request.args.get('attribute2')

    gdf = get_frameworkdata(vtc_url)
    adf = get_attributedata(attribute_url)
    keys = get_frameworkkey(framework_key, attribute1, attribute2)
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


app.run(debug=True, port=5000)  # run app in debug mode on port 5000
