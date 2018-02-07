from flask import Blueprint
from flask import request
from flask import Flask,redirect
import requests 
from flask import json
from flask import Flask, render_template
from flask import jsonify
from bs4 import BeautifulSoup
import time
import unicodedata
import csv

indigo = Blueprint("ind", __name__)


@indigo.route("/indigo/getindigo", methods = ['POST'])
def getindigo():
    try:
        res = request.json
        lastname =  request.form['lastName']
        pnr =  request.form['pnr']

        


        url = 'https://www.goindigo.in/#viewChangeBookingTab'
        payload = {}
        headers = {}
        response = requests.post(url, data=payload, headers=headers)
        cookies = response.cookies

        payload ["indiGoRetrieveBooking.EmailAddress"] = '' 
        payload ["indiGoRetrieveBooking.IndiGoRegisteredStrategy"] = 'Nps.IndiGo.Strategies.IndigoValidatePnrContactNameStrategy, Nps.IndiGo'
        payload ["indiGoRetrieveBooking.IsToEmailItinerary"] = 'false'
        payload ["indiGoRetrieveBooking.LastName"] = lastname
        payload ["indiGoRetrieveBooking.RecordLocator"] = pnr
        payload ["polymorphicField"] = lastname
        payload ["typeSelected"] = "SearchByNAMEFLIGHT"

        url = 'https://book.goindigo.in/Booking/Retrieve'
        response = requests.post(url, data=payload, cookies=cookies)
        cookies1 = response.cookies

        html = BeautifulSoup(response.content, 'html.parser')
        if html.find('div',{'class':'erro-info-title'}):
            return render_template('message.html', response_message = 302)
        elif html.find('div',{'class':'itiFlightDetails flights_table'}):
            if html.find('ul',{'class':'list-inline'}):
                list_flight = html.find('ul',{'class':'list-inline'})

                final_list= []
                name = list_flight.find('h2')
                x = []
                x.append(name.text.strip())
                final_list.append(x)
                filename = "final.csv"
                with open(filename, 'a+') as csvfile:
                    csvwriter = csv.writer(csvfile) 
                    csvwriter.writerows(final_list)
            return render_template('message.html', response_message = 202)

    


    except Exception as e:
        # print str(e)
        print (e)
        return render_template('message.html', response_message = 500)
    

