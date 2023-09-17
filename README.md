# TJS-Server: Table Joining Service for Vector Tiles Spatial Framework

The TJS-Server prototype was developed to explore the potential of utilizing vector tile caches as framework data for a Table Joining Service (TJS) API based on OGC standards. This project builds upon the MSC thesis by [Sharon Chawanji](https://www.linkedin.com/in/schawanji/), which can be found [on this link](https://cartographymaster.eu/wp-content/theses/2020_Chawanji_Thesis.pdf).

We are currently in the process of developing comprehensive documentation on how to use the API. You can visit the demo page [here](https://web-tjsenv.up.railway.app/) for a preview of its functionality. Please also visit the [Git repository](https://github.com/schawanji/TJS-Server-demonstrator) for an OpenLayers application to view the joined data. 

The TJS-Server API is built using Flask, a Python web framework for creating web apps and web services. Below, we describe the Flask route `joindata`, which provides the functionality to join GeoJSON and CSV data. To learn more about the OGC Table Joining Service, [please follow the link](https://www.ogc.org/standard/tjs/).

---

## Table of Contents

1. [Overview](#overview)
2. [Usage](#usage)
   - [Endpoint](#endpoint)
   - [Parameters](#parameters)
   - [Making an HTTP Request](#making-an-http-request)
   - [Response](#response)
3. [Examples](#examples)
   - [Example Request](#example-request)
   - [Example Response (GeoJSON)](#example-response-geojson)
4. [Error Handling](#error-handling)
5. [TJS-Server Linux Setup Guide](#tjs-server-linux-setup-guide)
   - [Prerequisites](#prerequisites)
   - [Installation and Setup](#installation-and-setup)
   - [Running the Server](#running-the-server)
   - [Accessing the Server](#accessing-the-server)
6. [Conclusion](#conclusion)

## Overview

This Flask-based API provides a simple way to join GeoJSON and CSV data based on user-provided parameters. It takes GeoJSON data from a specified URL, combines it with CSV data from another URL, and returns the merged data as a GeoJSON response. The merging is performed based on specified keys in the GeoJSON and CSV data.

## Usage

### Endpoint

**Endpoint URL**: `/tjs/api/joindata`

**HTTP Method**: GET

### Parameters

- **FrameworkURI**: URL of the GeoJSON data to be used as the framework for joining.
- **GetDataURL**: URL of the CSV data to be joined with the GeoJSON data.
- **FrameworkKey**: The key in the GeoJSON data that will be used for merging.
- **AttributeKey**: The key in the CSV data that corresponds to the `FrameworkKey` for merging.

### Making an HTTP Request

You can make a GET request to the `/tjs/api/joindata` endpoint by specifying the required parameters in the query string of the URL. Here's an example of how to make an HTTP request:

```http
GET /tjs/api/joindata?FrameworkURI=<GeoJSON_URL>&GetDataURL=<CSV_URL>&FrameworkKey=<GeoJSON_Key>&AttributeKey=<CSV_Key>
```

Replace the placeholders with the actual values:

- `<GeoJSON_URL>`: URL of the GeoJSON data to be used as the framework.
- `<CSV_URL>`: URL of the CSV data to be joined.
- `<GeoJSON_Key>`: The key in the GeoJSON data for merging.
- `<CSV_Key>`: The corresponding key in the CSV data for merging.

### Response

- If the request is successful and data is successfully merged, the API will respond with a GeoJSON representation of the merged data.
- If there is an issue with fetching the data or merging it, an error message with an appropriate HTTP status code will be returned.

## Examples

### Example Request

```http
GET /tjs/api/joindata?FrameworkURI=https://example.com/geojson_data.geojson&GetDataURL=https://example.com/csv_data.csv&FrameworkKey=geo_id&AttributeKey=id
```

### Example Response (GeoJSON)

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [125.6, 10.1]
      },
      "properties": {
        "name": "Location A",
        "value": 100
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [126.7, 11.2]
      },
      "properties": {
        "name": "Location B",
        "value": 200
      }
    }
  ]
}
```

## Error Handling

- If a required parameter is missing, the API will respond with an error message and a 400 Bad Request status code.
- If there are issues with fetching or merging data, the API will respond with an error message and a 500 Internal Server Error status code.

---

# TJS-Server Linux Setup Guide

This guide will walk you through setting up the TJS-Server project on a Linux-based system. Follow these steps to get the server up and running.

## Prerequisites

Before you begin, make sure you have the following installed on your Linux machine:

- [Git](https://git-scm.com/) for cloning the repository.
- [Python 3](https://www.python.org/) for running the server.
- [pip](https://pip.pypa.io/en/stable/) for managing Python packages.

## Installation and Setup

1. Clone the Repository:

   Use `git clone` to clone the TJS-Server repository to your local machine:

   ```bash
   git clone https://github.com/schawanji/TJS-Server.git
   ```

2. Create a Python Virtual Environment:

   Navigate to the project directory and create a Python virtual environment called `myenv`:

   ```bash
   cd TJS-Server
   python3 -m venv myenv
   ```

3. Activate the Virtual Environment:

   Activate the virtual environment using the following command:

   ```bash
   source myenv/bin/activate
   ```

4. Install Project Dependencies:

   Use `pip` to install the required Python packages listed in `requirements.txt`:

   ```bash
   pip install -U -r requirements.txt
   ```

## Running the Server

Now that you have set up the project and installed the dependencies, you can start the server by running the following command:

```bash
gunicorn main:app
```

The server should start, and you will see a message indicating that it's running on `http://127.0.0.1:8000`.

## Accessing the Server

You can access the server by opening a web browser and navigating to the following URL:

```
http://127.0.0.1:8000
```

This is the local address where the server is running. If you want to access it from other devices on the same network, replace `127.0.0.1` with your Linux machine's IP address.

## Conclusion

You have successfully set up and run the TJS-Server project on your Linux system. You can now use and test the server as needed. If you encounter any issues or have questions, feel free to reach out for assistance.


