 
# Se importan las Librerías: 'socket'-interfaz que permite la comunicación entre 
#                             procesos de diferentes máquinas.
#                           'threading' -módulo para crear y gestionar hilos.

import os
import socket
import threading

# Se determina puerto y dirección de conexión del servidor 
host = "127.0.0.1"
port = 8050


# Se crea un socket [socket.AF_INET: especifíaca el dominio del socket siendo en este caso IPv4.]
#                   [socket.SOCK_STREAM: define el tipo de socket, en este caso se basa en protocolo 
#                   TCP(significa que ofrece la seguridad de la llegada en orden de los paquetes y 
#                   descarta repetición o daños de los mismos.)]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# .bind permite la conexión asociando un puerto y una dirección las cuales se 
# pasan por parámetros 'host'-'port'.

server.bind((host, port))


# Esto prepara al socket a recibir conexiones entrantes, el argumento '5' especifica el 
# tamaño de la cola de espera, es decir: número máximo de conexiones pendientes.

server.listen(5)
print("\nSERVER >> Running on:")

print("Address: {} \nPort: {}\n".format(host, port))
print("SERVER >> listening...")

# Lista de clientes y lista de nombres de usuarios de los mismos.

clientes =[]
usuarios = []


# Función para relacionar la lista de cliente con el cliente que envía mensaje, por esta
# función se puede detectar que cliente envía mensaje para que el servidor no le comparta
# el mensaje a él sino que lo haga a todos los otros clientes.

def mensajesEnvios(datosMensajes, _cliente):
  for cliente in clientes:
    if cliente != _cliente:
      cliente.send(datosMensajes)


# Función que recibe el mensaje del cliente una vez haya sido aceptado su enlace con el servidor.
# Esta función llama a la funciónn "mensajeEnvios" para comparar los clientes que envían los mennsajes
# también permite borrar al cliente en caso de darse como desconectado del servidor.

def mensajesClientes(cliente, direccion, usuario):

    while True:
      try:
        print("connection data; \n{}.".format(cliente))
        conectado = cliente.send("SERVER >> Bienvenido/a al sistema de comunicación Server/Client!!!\nSERVER >> Para 'Salir' ingrese palabra clave 'quit'\n".encode('UTF-8'))
        while True:
          if cliente:
            datosMensajes = cliente.recv(4096)
            mensajesEnvios(datosMensajes, cliente)    
          else:
            indexListaClientes = clientes.index(cliente)
            usuarioCliente = usuarios[indexListaClientes] 
            mensajesClientes(f'[Mensaje-Servidor]>> {usuarioCliente} Desconectado'.encode("utf-8"))
            clientes.remove(cliente)
            usuarios.remove(usuarioCliente)
# Sección de except para tomar el Error ejecutado por el sistema al momento de desconectarse del cliente.
      except:
        print("\nCerrando enlace Server/Client")
        break
# finally forma parte del bucle while, por lo tanto se coloca pero con argumento "pass" para que no tenga una función específica.
      finally:
        pass
# Bucle infinito while, se utiliza para dar como cerrada la sesión con el cliente pero en espera y escucha para nuevas conexiones.
    while True:
      print("\nSERVER >> Running on:")
      print("Address: {} \nPort: {}\n".format(host, port))
      print(f'''-------------------------------------------------------------------------------
                 {usuario}: {str(direccion)}, Cerrando sesión...
-------------------------------------------------------------------------------''')
      indexListaClientes = clientes.index(cliente)
      usuarioCliente = usuarios[indexListaClientes] 
      mensajesClientes=print(f"SERVER >> {usuarioCliente} Desconectado!!!".encode("utf-8"))
      clientes.remove(cliente)
      usuarios.remove(usuarioCliente)
      print("SERVER >> listening...")
      cliente.close()
      break


# Función para dar de alta las conexiones con los diversos clientes, generación de hilo para la función de mensajes entrantes
# y datos proporcionados al cliente desde el lado del servidor.

def conectar():
# Acepta conexión con cliente.
    while True:
      cliente, direccion = server.accept()
# Solicitud a cliente de ingreso de usuario.
      cliente.send("@usuario".encode('utf-8'))
      usuario = cliente.recv(4096).decode('utf-8')
# Se ingresan los usuarios en las listas "clientes" y "usuarios"
      clientes.append(cliente)
      usuarios.append(usuario)
# Informa en pantalla de servidor la conexión autorizada con el cliente.
      print(f'[CLIENTE {usuario}] se conecto con {str(direccion)}')
# Informa a los clientes ya ingresados en la sala de chat, quien se agregó a la misma.
      mensaje = f'\nSERVER >> {usuario} Conectado a Chat...'.encode("utf-8")
# Se envía al cliente la leyenda de conexión correcta con el servidor.
      mensajesEnvios(mensaje, cliente)
      cliente.send("SERVER >> Conectado al Servidor...".encode('utf-8'))
# Se crea el hilo, mediante la librería importada "threading" para la función "mensajesClientes".
      threading.Thread(target=mensajesClientes, args=(cliente,direccion, usuario)).start()
# Se llama a la función conectar.
conectar()