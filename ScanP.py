# Port Scanner
# A simple port scanner written in Python using the socket library.

import socket
from tqdm import tqdm

openPorts = []

def scan_port(targetIP, port):
    try:
        # Crear un objeto
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        # Establecer un tiempo de espera para la conexión
        s.settimeout(1)
        # Intentar conectar al puerto
        s.connect((targetIP, port))
        # Si no hay excepción, el puerto está abierto 
        print(f"Port {port} is open")
        openPorts.append(port) # Agregar el puerto a la lista de openPorts
    except socket.error:
        # Si hay excepción, el puerto está cerrado
        print(f"Port {port} is closed")
    finally:
        # Cerrar la conexión
        s.close()

# Solicitar al usuario ingresar la dirección IP         
targetIP = str(input("Ingresa la dirección IP: "))

# Solicitar al usuario ingresar los puertos a escanear
startPort = int(input("Ingresa el puerto inicial del rango a escanear: "))
endPort = int(input("Ingresa el puerto final del rango a escanear: "))

# Usar tqdm para mostrar la barra de progreso
with tqdm(total=endPort - startPort + 1, desc="scanning ports") as pbar:
    for port in range(startPort, endPort + 1)
    scan_port(targetIP, port)
    pbar:update(1) # Actualizar la barra de progreso

# Escanear los puertos especificados y generar el informe
print("\nPuertos abiertos: ")
for port in openPorts:
    print(f"Puerto {port} está abierto")
