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
            return render_template('message.html', response_message = 302, base_url = globals.base_url)
        elif html.find('div',{'class':'itiFlightDetails flights_table'}):
            if html.find('ul',{'class':'list-inline'}):
                list_flight = html.find('ul',{'class':'list-inline'})

                final_list= []
                names = list_flight.find_all('h2')
                x = []
                finalname = ''
                for name in names:
                    finalname = finalname +  name.text.strip() + ','
                x.append(finalname)
                x.append(str(datetime.datetime.now()))
                flight_all_details = html.find('div',{'class':'itiFlightDetails flights_table'})
                flight_all_details = flight_all_details.find('table')
                flight_all_details = flight_all_details.find('tbody')

                flight_detail = flight_all_details.find_all('tr')

                if len(flight_detail) == 1:
                    flight = flight_detail.find_all('td')
                    for f in flight:
                        x.append(f.text.strip())
                    # k = flight_details.text.strip()
                    # k = k.split('\n')
                    # print (k)
                    # if len(k) >= 10:
                    #     x.append(k[0])
                    #     x.append(k[1])
                    #     x.append(k[2])
                    #     x.append(k[3])
                    #     x.append(k[4])
                    #     x.append(k[5])
                    #     x.append(k[6])
                    #     x.append(k[7])
                    #     x.append(k[8])
                    #     x.append(k[9])
                elif len(flight_detail) >1:
                    flight = flight_detail[0].find_all('td')
                    for f in flight:
                        x.append(f.text.strip())

                    destination = flight_detail[len(flight_detail)-1].find_all('td')
                    x[6] = destination[4].text.strip()

                final_list.append(x)
                filename = "final.csv"
                with open(filename, 'a+') as csvfile:
                    csvwriter = csv.writer(csvfile) 
                    csvwriter.writerows(final_list)
            return render_template('message.html', response_message = 202, base_url = globals.base_url)
        else:
            return render_template('message.html', response_message = 500 , base_url = globals.base_url)



    


    except Exception as e:
        # print str(e)
        print (e)
        return render_template('message.html', response_message = 500, base_url = globals.base_url)
    

