# metrobus
api para consultar datos del metrobus

instrucciones de uso:

instalar las dependencias

correr mongod desde terminal

correr create_update_dbs.py

correr app.py

en Postman hacer las llamadas de la siguiente manera:

para obtener las unidades disponibles:

GET http://127.0.0.1:5000/disponible

para consultar el historial de ubicaciones dado el id:

GET http://127.0.0.1:5000/historial_unidad/1235

para obtener la lista de alcaldías:

GET http://127.0.0.1:5000/alcaldias

para obtener la lista de unidades disponibles por alcaldía:

GET http://127.0.0.1:5000/disponible_alcaldia/Iztacalco