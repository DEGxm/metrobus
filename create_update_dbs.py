import requests
import pymongo

client = pymongo.MongoClient("localhost", 27017)

client.drop_database('alcaldias')
db = client.alcaldias
collection = db.polygon

alcaldias = requests.get("https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=limite-de-las-alcaldias&q=&rows=16&facet=nomgeo").json()["records"]

for i in alcaldias:
    print('#####')
    i['fields']['geo_shape']['coordinates'][0] = [tuple(u) for u in i['fields']['geo_shape']['coordinates'][0]]
#    print(i['fields']['geo_shape']['coordinates'][0])
#    print(i['fields']['nomgeo'])
    alcaldia = {
            'polygon': i['fields']['geo_shape']['coordinates'][0],
            'name': i['fields']['nomgeo']
            }
    print(alcaldia)
    collection.insert_one(alcaldia)

records = requests.get("https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=prueba_fetchdata_metrobus&rows=300&q=").json()["records"]

db = client.metrobusdb
collection = db.location

for record in records:
    try:
        collection.insert_one(record)
    except Exception as e:
        print(e)