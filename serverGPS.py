"""
----------------------------------------------------------------------
#Universidad del Valle de Guatemala
#Megaproyecto LAGO
#Código adaptado y corregido por José Pablo Ortega Grajeda
#Lectura de GPS
#Módulo GPS utilizado: RPI Add-on V2.0
----------------------------------------------------------------------
"""
import socket
import time
#import serial
import subprocess as sub
#import shlex
import ast
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

ser = 0

class Socket:
    """
    Socket generico
    """

    sock = None
    
    def __init__(self, sock): #Singleton
        if sock is None:
            #Crear uno nuevo
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            #Setear el socket
            self.sock = sock
    def bind(host, port):
        #Deberia ser bind((socket.gethostname()
        self.sock.bind((host, port))
        self.sock.listen(5);

    def connect(self, host, port):
        #Abrir una conexion TCP a la maquina host en el puerto port
        self.sock.connect((host, port))

    def write(self, msg):
        #Mandar el mensaje msg al host que estemos conectados
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(bytes(msg[totalsent:]))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def read(self):
        #Recibir mensaje 
        chunks = []
        bytes_recd = 0
        done = False
        while not done:
            chunk = self.sock.recv(4096)
            if chunk == '':
                raise RuntimeError("socket connection broken")
                done = True
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
            if b'$' in chunk:
                done = True
        #print(''.join(chunks))
        print(b''.join(chunks).decode(encoding='UTF-8'))
        #return #b''.join(chunks).decode(encoding='UTF-8')


##---------Lectura Serial de GPS - Puerto 15 ttyAMA0-------------
def init_serial():
    COMNUM = 10
    global ser
    ser = serial.Serial()
    ser.baudrate = 9600
    #ser.port = CONUM # es el 10 o puerto 15
    ser.port = '/dev/ttyAMA0' 
    
    #timeout
    ser.timeout = 15
    ser.open() #abrir puerto GPS
    if ser.isOpen():
        print 'GPS Open...'

##---------------------------------------------------------------

##Programa principal de la Raspberry pi
"""
Protocolo de envio
Se necesita enviar un identificador, temperatura, gps, tiempoFecha, data
la fecha dependera de si mandamos el long o no y GMT
LAGO
25.22
123 23 59
17/03/2016 14:56:51
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
OGAL
"""
#----------------------------------------------------------------#
#init_serial() #iniciar puerto GPS
#socket_cliente = Socket(None)
#socket_cliente.connect("172.20.14.178",1111) #Iniciar conexion server PC


#while True:
    #gps_data = ser.readline() #leer data de gps
    
#Ejecutar comando y leer output
p1 = sub.Popen(["gpspipe", "-w", "-n", "6"], stdout=sub.PIPE)
p2 = sub.Popen(["grep", "-m", "1", "TPV"], stdin=p1.stdout, stdout=sub.PIPE) # pipe grep TDV

#lat = sub.Popen(shlex.split("jsawk 'return this.lat'"), stdin=p2.stdout, stdout=sub.PIPE)
#lat = sub.Popen(["jsawk", "return this.lat"], stdin=p2.stdout, stdout.sub.PIPE)

out, err = p2.communicate()  #leer output terminal
raw = ast.literal_eval(out)
lat = str(raw['lat'])
lon = str(raw['lon'])

mensaje = "LAGOUVG$$temperatura$$Lat: "+lat+" Lon: "+lon+"$$"+time.strftime("%c")+"$$bin1 bin2 bin3 ...$$OGAL\n"

#mensaje = time.strftime("%c")
#mensaje = "pela la verga\n"
print(mensaje)

#socket_cliente.write(mensaje)
#socket_cliente.read()
#confirmacion = socket_cliente.read()
#print confirmacion
#time.sleep(5) #esperar x segundos

