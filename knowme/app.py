# import necessary libraries
import os
from flask import Flask, render_template,  jsonify, request
import numpy as np
import pandas as pd


# Create an instance of our Flask app.
app = Flask(__name__)


# Flask Routes
#List all routes that are available
@app.route("/")
def welcome():
    """Return the homepage."""
    return render_template("index.html")
   
    
if __name__ == "__main__":
    app.run(debug=True)
