##############################################################################################################

# TP Especial Redes de Computadoras - FI UNMDP - 2020
# Alumnos: Mariquena Gros - Pablo Porzio

# correr como admin

##############################################################################################################

from scapy.all import ARP, Ether, srp
from cmd import Cmd 
import datetime, threading, time, json, sys

# base de datos de empleados

class Empleado:
	def __init__(self, nombre, mac):
		self.nombre = nombre
		self.mac = mac
		self.ultimaAparicion = datetime.datetime(2010,12,4,06,0,0,0) # fecha vieja x defecto
		self.online = False 

class BaseDatos:
	def __init__(self, datosEmpleado, plazoMax):
		self.plazoMax = plazoMax
		self.bd = {}
		
		for mac, nombre in datosEmpleado.iteritems():
    			self.bd.update({mac: Empleado(nombre, mac)})

	def actualizarAparicion(self, mac, timestamp):
		empleado = self.bd.get(mac)
		if empleado != None: # descarta dispositivos no registrados
			empleado.ultimaAparicion = timestamp
			empleado.online = True

	def estaOnline(self, mac):
		empleado = self.bd.get(mac)

		empleado.online = ((datetime.datetime.now() - empleado.ultimaAparicion).total_seconds() <= self.plazoMax) 

		return empleado.online

	def agregarEmpleado(self, mac, nombre):
		if (self.bd.get(mac) == None):
			self.bd.update({mac: Empleado(nombre, mac)})
		else:
			print('MAC ya registrada!!')

	def mostrarTodos(self):

		print("NOMBRE"+" "*18+"MAC"+" "*21+"ULTIMA APARICION"+" "*8+"ESTADO")
		
		for empleado in self.bd.values():
			estado = 'online' if self.estaOnline(empleado.mac) else 'offline'
	    		print("{:19}     {:20}    {:20}    {}".format(empleado.nombre, empleado.mac, empleado.ultimaAparicion.strftime("%H:%M:%S"), estado))
	
	def guardarCambios(self):
		
		persistencia = {}		
		
		for empleado in self.bd.values():
			persistencia.update({empleado.mac : empleado.nombre})

		json.dump(persistencia,open('empleados.json', "w"))
   			
# scanea red para descubrir celulares conectados periodicamente

def scanner(bd, lan, periodo):

	prox = time.time()	

	while True:
		
		# creacion trama de capa 2 para broadcast con solicitud ARP 
		arp = ARP(pdst=lan)
		ether = Ether(dst="ff:ff:ff:ff:ff:ff")
		paquete = ether/arp

		# envio de paquetes en capa 2
		resultado = srp(paquete, timeout=3, verbose=0)[0]

		# actualizacion de estados
		for enviado, recibido in resultado:
	    		bd.actualizarAparicion(recibido.hwsrc, datetime.datetime.now()) # mac de conectado y timestamp actual
		
		# hilo duerme hasta prox pasada
		prox = prox + periodo;
		time.sleep(prox - time.time())

# main

def main():

	config = json.load(open("config.json"))
	bd = BaseDatos(json.load(open("empleados.json")), config['plazoMax'])

	hilo = threading.Thread(target=scanner, args=[bd, config['lan'], config['periodoControl']])
	hilo.daemon = True
	hilo.start()

	class MyPrompt(Cmd):
	    prompt = 'scanner> '
	    intro = "Bienvenido! Ingrese ? o help para listar los comandos"

	    def do_listar(self, inp):
		'Muestra los datos de todos los empleados y su estado de conexion.'
		bd.mostrarTodos()
	 
	    def do_agregar(self, inp):
		'Cargar un nuevo empleado en la BD. Ingresar mac/nombre.'
		nuevoEmpleado = inp.split('/')		
		bd.agregarEmpleado(nuevoEmpleado[0], nuevoEmpleado[1])
	    
	    def do_salir(self, inp):
		'Cierre de aplicacion y persiste los empleados ingresados.'
		bd.guardarCambios()
		print("Adios :)")
		sys.exit()
		return True

	MyPrompt().cmdloop()

main()








