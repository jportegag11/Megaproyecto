#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Codigo envio de datos desde reserva hacia UVG Sur

@author: Daniela Pocasangre & Jose Pablo Ortega
"""

import paramiko
import os
import bz2

import time, datetime

username = 'pi' 
port = 22 #ssh
password = #password
hostname = '192.168.1.5'

directorio = os.getcwd()

a=1

if(a==1 and datetime.datetime.now().minute==35):
    try:      
        ssh = paramiko.SSHClient()        #open ssh
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(hostname, port=port, username=username, password=password)
    
        sftp = ssh.open_sftp()    
        
        sftp.chdir('/home/pi/Desktop/')
        
        lista = sftp.listdir()
        lista.sort(reverse=True)
        
        for i in range(len(lista)-1):
            files = str(lista[i])
            
            localpath = directorio+'/'+files #local path - UVG Sur
            
            remotepath = '/home/pi/Desktop/'+files #remote path - Raspberry
        
            sftp.get(remotepath, localpath) #get file from rasp to uvg sur
		
            
            #sftp.remove('/home/pi/Desktop/' + files) #delete trasmitted file from folder
    
        sftp.close()
        ssh.close()
        
    except Exception, e:
        print str(e)

    #modify .dat - lista[0]
	
	with open(lista[0],'r') as file:
		estado = file.readlines()
	
	temp = estado[0];
	pres = estado[1];
	
	
	with open(lista[0],'r') as file:
			data = file.readlines()

		data[13] = "# #   # x s " + str(temp) + " C " + str(pres) + " hPa 1582 m : temperature <T>, pressure <P> and altitude (from pressure) <A>\n"
		data[14] = "# #   # x g 14.548006 -91.193671 1582   : GPS data - latitude, longitude, altitude"


		with open(enviar[0],'w') as file:
			file.writelines(data)
			
		"""FIN DE REESCRITURA DE ARCHIVOS"""

    #compress .dat - list[0]

    bz2content = bz2.compress(open(directorio+'/'+files,'rb').read(), 9)
    
    lista[0] = lista[0] + '.bz2'
    
    fh = open(directorio+'/'+files, 'wb')   
    fh.write(bz2content)
    fh.close()
