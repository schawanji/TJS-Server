## TJS-Server: Table Joining Service for Vector Tiles Spatial Framework

The TJS-Server prototype was developed to explore the potential of utilizing vectortile caches as framework data for a TJS API based on OGC standards. This project builds upon the MSC thesis by Sharon Chawanji, which can be found [here](https://cartographymaster.eu/wp-content/theses/2020_Chawanji_Thesis.pdf).

We are currently in the process of developing comprehensive documentation on how to use the API. You can visit the demo page [here](https://schawanji.herokuapp.com/) for a preview of the functionality.

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
python app.py
```

The server should start, and you will see a message indicating that it's running on `http://127.0.0.1:5000`.

## Accessing the Server

You can access the server by opening a web browser and navigating to the following URL:

```
http://127.0.0.1:5000
```

This is the local address where the server is running. If you want to access it from other devices on the same network, replace `127.0.0.1` with your Linux machine's IP address.

## Conclusion

You have successfully set up and run the TJS-Server project on your Linux system. You can now use and test the server as needed. If you encounter any issues or have questions, feel free to reach out for assistance.


