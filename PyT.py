"""
----------------------------------------------------------------------
#Universidad del Valle de Guatemala
#Megaproyecto LAGO
#Código adaptado y corregido por José Pablo Ortega Grajeda
#Lectura de sensor de PyT a través de protocolo I2C en Raspberry Pi
#Sensor de PyT utilizado: LPS331AP MEMS
#Datasheet disponible en: 
----------------------------------------------------------------------
"""
from smbus import SMBus
import time

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

#Se piden los valores del temperatura del sensor
templow = bus.read_byte_data(PyT, TEMP_OUT_L)
temphigh = bus.read_byte_data(PyT, TEMP_OUT_H)

templow = bin(templow)[2:]
temphigh = bin(temphigh)[2:]
temp = temphigh + templow

#Se hace la conversión para tener temperatura en grados centígrados
temp = comp2(int(temp,2), len(temp))
temp = 32.5 + (temp/480)
print "la temperatura es: " + str(temp) + "C"

#Se piden los valores de presión del sensor
presxl = bus.read_byte_data(PyT, PRESS_OUT_XL)
presl = bus.read_byte_data(PyT, PRESS_OUT_L)
presh = bus.read_byte_data(PyT, PRESS_OUT_H)

presxl = hex(presxl)[2:]
presl = hex(presl)[2:]
presh = hex(presh)[2:]
pres = presh + presl + presxl

#Se hace la conversión para tener la presión en mbar
pres = int(pres,16)
pres = pres/4096
print "la presion es: " + str(pres) + "mbar"
