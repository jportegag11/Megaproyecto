#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#Universidad del Valle de Guatemala
#Megaproyecto LAGO
#Código creado por Daniela Izabel Pocasangre Arévalo y José Pablo Ortega Grajeda
#Lectura de sensores, manejo de archivos de datos y envío automático

import paramiko
import os
from smbus import SMBus
import time
import time, datetime
import Adafruit_DHT

dateString = '%Y/%m/%d %H:%M:%S'
sensor = Adafruit_DHT.DHT11
pin = 4

#SSH
username = 'Lagouvg' 
port = 22 #ssh
password = 'Lagouvg'
hostname = '192.168.1.7'

enviando = False

while(True):
	minuto = datetime.datetime.now()strftime("%M")
	segundo = datetime.datetime.now()strftime("%S")
	if (int(minuto) == 0 and int(segundo) == 0):

		"""SENSOR DE HUMEDAD"""
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		fecha = datetime.datetime.now().strftime(dateString)
		f = open("estado.txt","w")
		f.write("Fecha: ",fecha, "Humedad: ", humidity, "Temperatura : ", temperature)
		f.close()
		"""FIN SENSOR HUMEDAD"""	


		"""SENSOR DE PyT"""

		#Direcciones de registros importantes
		bus = SMBus (1)
		PyT = 0x5c		#Direccion del PyT
		CTRL_REG1 = 0x20	#Registro de control
		WHO_AM_I = 0x0F		#Registro de validacion
		STATUS_REG = 0x27	#Registro de estado

		PRESS_OUT_XL = 0x28	#Registros de presion
		PRESS_OUT_L = 0x29
		PRESS_OUT_H = 0x2A

		TEMP_OUT_L = 0x2B	#Registros de temperatura
		TEMP_OUT_H = 0x2C

		#Funcion para cambio de complemento a dos
		def comp2 (val, bits):
			if (val & (1 << (bits - 1))) != 0:	#Si tiene signo se opera
				val = val - (1 << bits)
			return val


		#bus.write_byte_data(PyT, CTRL_REG1, 0x90) #Set a los valores iniciales del sensor
		#ctrl = bus.read_byte_data(PyT,CTRL_REG1)
		#print ctrl

		#william = bus.read_byte_data(PyT, WHO_AM_I)
		#print william

		templow = bus.read_byte_data(PyT, TEMP_OUT_L)
		temphigh = bus.read_byte_data(PyT, TEMP_OUT_H)

		templow = bin(templow)[2:]
		temphigh = bin(temphigh)[2:]
		temp = temphigh + templow


		temp = comp2(int(temp,2), len(temp))
		temp = 32.5 + (temp/480)
		print "la temperatura es: " + str(temp) + "C"

		presxl = bus.read_byte_data(PyT, PRESS_OUT_XL)
		presl = bus.read_byte_data(PyT, PRESS_OUT_L)
		presh = bus.read_byte_data(PyT, PRESS_OUT_H)

		presxl = hex(presxl)[2:]
		presl = hex(presl)[2:]
		presh = hex(presh)[2:]
		pres = presh + presl + presxl


		pres = int(pres,16)
		pres = pres/4096
		print "la presion es: " + str(pres) + "mbar"

		"""FIN SENSOR DE PyT"""

		"""REESCRITURA DE ARCHIVOS .dat CON DATOS DE LOS SENSORES"""

		lagoarchivos = os.listdir('/home/pi/acqua/brc/lago')
		lagoarchivos.sort(reverse=True)
				
		directorioactual = os.getcwd()
				
		os.rename('/home/pi/acqua/brc/lago/' + lagoarchivos[0], directorioactual + '/' + lagoarchivos[0])

		enviar = os.listdir(directorioactual) #files on directory
		enviar.sort(reverse=True)

		with open(enviar[0],'r') as file:
			data = file.readlines()

		data[13] = "# #   # x s " + str(temp) + " C " + str(pres) + " hPa 1582 m : temperature <T>, pressure <P> and altitude (from pressure) <A>\n"
		data[14] = "# #   # x g 14.548006 -91.193671 1582   : GPS data - latitude, longitude, altitude"


		with open(enviar[0],'w') as file:
			file.writelines(data)
			
		"""FIN DE REESCRITURA DE ARCHIVOS"""

		"""ENVIO DE DATOS"""

		if(enviando==True):
			try:      
				ssh = paramiko.SSHClient()        #open ssh
				ssh.load_system_host_keys()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				
				ssh.connect(hostname, port=port, username=username, password=password)
			
				sftp = ssh.open_sftp()    
			
				for i in range(len(directorioactual)-1)
					remotepath = '/home/lagouvg/Escritorio' + enviar[i] #remote path - UVG Sur 
					localpath = directorioactual + '/' + enviar[i] #local path - rasp
					sftp.put(localpath, remotepath) #send file from rasp to UVG Sur

					#os.remove(directorioactual + '/' + enviar[i]) #delete trasmitted file from folder

				sftp.close()
				ssh.close()
				
			except Exception, e:
				print str(e)
