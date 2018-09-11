"""
----------------------------------------------------------------------
#Universidad del Valle de Guatemala
#Megaproyecto LAGO
#Código creado por José Pablo Ortega Grajeda
#Lectura de sensor de presión y humedad
#Sensor de humedad y temperatura utilizado: módulo DHT22
#Datasheet disponible en: https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf
----------------------------------------------------------------------
"""
import time, datetime
import Adafruit_DHT

dateString = '%Y/%m/%d %H:%M:%S'
sensor = Adafruit_DHT.DHT11
pin = 4

#El siguiente bucle se realiza cada segundo. En él, se lee el valor de humedad y temperatura del
#sensor, se obtiene la hora y fecha actual, y se escribe en una nueva línea del archivo de texto
#y luego se cierra el archivo
while True:
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	fecha = datetime.datetime.now().strftime(dateString)
	f = open("estado.txt","w")
	f.write("Fecha: ",fecha, "Humedad: ", humidity, "Temperatura : ", temperature)
	f.close()
	time.sleep(1);
	hon_DHT.gi