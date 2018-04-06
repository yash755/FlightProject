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

goair = Blueprint("goair", __name__)


@goair.route("/goair/getgoair", methods = ['POST'])
def getgoair():
    try:
        res = request.json
        lastname =  request.form['lastName']
        pnr =  request.form['pnr']

        url1 = 'https://book.goair.in/Booking/Index?rl=' +  str(pnr) + '&ln='+  str(lastname)
        response1 = requests.get(url1)
        html = BeautifulSoup(response1.content, 'html.parser')
        filename = open('ram.txt','a+')
        filename.write(str(html))
        filename.close()
        return lastname

        

    except Exception as e:
        # print str(e)
        print (e)
        return render_template('message.html', response_message = 500, base_url = globals.base_url)
    

