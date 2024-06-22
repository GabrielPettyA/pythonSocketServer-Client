#------------------------------------------------ CODIFICACIÓN LADO CLIENTE -----------------------------------------
# Importación de librería.
import os
import socket
import sys
import threading

# Se ingresa el usuario solicitado desde el lado del servidor.
usuario = input("Ingrese Usuario: ").upper()
# Se declaran la dirección y el puerto utilizado para conexión con servidor.
host = "127.0.0.1"
port = 8050

#  Se genera un objeto utilizando la librería de socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se realiza la conexión del objeto socket generado con la dirección y puerto declarados anteriormente.
cliente.connect((host, port))
#print("\nCLIENTE CONECTADO >>")

# Función para enviar al servidor el nombre del usuario solicitado y los mensajes a compartir con el chat.
def recibirMensaje():
  
  while True:
# Se carga y envía el usuario que solicitó el servidor y que se cargó con anterioridad en celda Nro.8 .
      try:
        mensaje = cliente.recv(4096).decode('utf-8')
        if mensaje == "@usuario":
          cliente.send(usuario.encode('utf-8'))
# Se envía mensajes ingresados para chat con clientes.
        else:
          print(mensaje)
# Se toma error en caso de desconexión.
      except:
        print("Cerrando conexión...")
        break
# Se envía mensaje al cliente de la finalización del cierre de sesión.
  print("Conexión cerrada !!!")

# Función relacionada al ingreso de los mensajes para sección chat y creación de hilos relacionados a los mensajes.
def tuMensaje():
  while True:
    mensaje = f"{usuario}: "
    initmensaje= input("")
    todo= mensaje + initmensaje
# Sección para realizar los diferentes parámetros relacionados a los mensajes ingresados.
    if initmensaje == 'quit' or initmensaje == 'QUIT' or initmensaje == 'Quit':
      os.system('cls')
      men = f"{mensaje} Desconectando..."
      print(men)
      cliente.close()
      sys.exit(0)
    
    if initmensaje == '':
      print("Recuerde ingresar mensaje.")
    
    if initmensaje != 'quit':
      cliente.send(todo.encode('utf-8'))
# Generación de los hilos correspondientes a las funciones "recibirMensaje" y "tuMensaje".
threading.Thread(target=tuMensaje).start()
threading.Thread(target=recibirMensaje).start()
