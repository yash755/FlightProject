from flask import Flask, render_template
from flask import request
import requests 
import globals
from flask import json
from flask import jsonify
from bs4 import BeautifulSoup
from indigo import indigo

app = Flask(__name__)
app.register_blueprint(indigo)



@app.route("/")
def main():
	return render_template('index.html', base_url = globals.base_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5005"),debug = True)