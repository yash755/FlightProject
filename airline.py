from flask import Blueprint
from flask import request
from flask import Flask,redirect
import requests 
import globals
from flask import json
from flask import Flask, render_template
from flask import jsonify
from bs4 import BeautifulSoup
import time
import unicodedata
import csv
import datetime

airline = Blueprint("air", __name__)


@airline.route("/airline", methods = ['POST'])
def getairline():
    try:
        res = request.json
        airline =  request.form['airline_name']

        if airline == 'indigo':
             return render_template('indigo.html', base_url = globals.base_url, type = 'Indigo')
        elif airline == 'goair':
            return render_template('goair.html', base_url = globals.base_url, type = 'GoAir')
        else:
            return lastname;


        #     return render_template('message.html', response_message = 202, base_url = globals.base_url)
        # else:
        #     return render_template('message.html', response_message = 500 , base_url = globals.base_url)



    


    except Exception as e:
        # print str(e)
        print (e)
        return render_template('message.html', response_message = 500, base_url = globals.base_url)
    

