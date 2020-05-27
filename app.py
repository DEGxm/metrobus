# -*- coding: utf-8 -*-
"""
Created on Tue May 26 22:39:20 2020

@author: dario
"""
# ><

from flask import Flask
from flask_pymongo import PyMongo
import pymongo
from datetime import timedelta, datetime
import requests
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

client = pymongo.MongoClient("localhost", 27017)

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'metrobusdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/metrobusdb'

mongo = PyMongo(app)


@app.route('/disponible', methods=['GET'])
def get_available_units():
    location = mongo.db.location
    output = {
        'status': 200,
        'message': 'success',
        'data': ''}

    records = requests.get(
        "https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=prueba_fetchdata_metrobus&rows=300&q=").json()[
        "records"]

    db = client.metrobusdb
    collection = db.location
    datetime_str = ''

    for record in records:
        try:
            collection.insert_one(record)
        except Exception as e:
            print(e)

    print('las siguientes unidades están disponibles')
    available = []
    for s in location.find({'fields.vehicle_current_status': 2}):  # asuming that status 2 means available
        try:
            datetime_str = s['fields']['date_updated']
            datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

            if datetime_object < datetime.utcnow() + timedelta(seconds=-20):
                available.append(s['fields']['vehicle_id'])
                #print(s['fields']['geographic_point'])
        except Exception as e:
            print(e)
    output['data'] = available
    return output


@app.route('/historial_unidad/<unit_id>', methods=['GET'])
def get_unit_history(unit_id):
    location = mongo.db.location
    output = {
        'status': 200,
        'message': 'success',
        'data': ''}
    Data = []
    for s in location.find({'fields.vehicle_id': unit_id}):
        try:
            data = {
            }
            data['record_timestamp'] = s['record_timestamp']
            data['trip_start_date'] = s['fields']['trip_start_date']
            data['geographic_point'] = s['fields']['geographic_point']
            Data.append(data)
        #        print(s['record_timestamp'],s['fields']['trip_start_date'],s['fields']['geographic_point'])
        except Exception as e:
            print(e)
    output['data'] = Data
    return output


@app.route('/alcaldias', methods=['GET'])
def get_buroughs():
    db = client.alcaldias
    collection = db.polygon
    output = {
        'status': 200,
        'message': 'success',
        'data': ''}
    names = []
    for s in collection.find():
        try:
            names.append(s['name'])
        #            print(s['polygon'])
        #            for i in s['polygon']:
        #                print('yolo',tuple(i))
        except Exception as e:
            print(e)
    output['data'] = names
    return output


@app.route('/disponible_alcaldia/<alcaldia>', methods=['GET'])
def get_units_in_burough(alcaldia):
    #print(alcaldia)
    location = mongo.db.location
    output = {
        'status': 200,
        'message': 'success',
        'data': ''}

    records = requests.get(
        "https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=prueba_fetchdata_metrobus&rows=300&q=").json()[
        "records"]

    db = client.metrobusdb
    collection = db.location
    datetime_str = ''

    for record in records:
        try:
            collection.insert_one(record)
        except Exception as e:
            print(e)
    available = []
    for s in location.find({'fields.vehicle_current_status': 2}):  # asuming that status 2 means available
        try:
            datetime_str = s['fields']['date_updated']
            datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

            if datetime_object < datetime.utcnow() + timedelta(seconds=-20):
                available.append([s['fields']['vehicle_id'], s['fields']['geographic_point']])
        except Exception as e:
            print(e)

    db = client.alcaldias
    collection = db.polygon
    output = {
        'status': 200,
        'message': 'success',
        'data': ''}
    alcaldias = []
    for s in collection.find():
        try:

            #          print(s['polygon'])
            tuple_polygon = []
            for i in s['polygon']:
                tuple_polygon.append(tuple(i))
            #              print('yolo',tuple(i))
            alcaldias.append([s['name'], tuple_polygon])
        except Exception as e:
            print(e)

    Available = []
    A = [i[0] for i in alcaldias]
    B = A.index(alcaldia)
    #  print('wolololo',alcaldias[B][0])
    for t in available:
        point = Point(t[1][1], t[1][0])
        poly = Polygon(alcaldias[B][1])
        if poly.contains(point) == True:
            Available.append(t)
    output['data'] = Available

    return output


if __name__ == '__main__':
    app.run(debug=True)