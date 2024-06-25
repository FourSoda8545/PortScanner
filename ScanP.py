# Escáner de Puertos
# Un escáner de puertos simple escrito en Python utilizando la biblioteca socket.

import socket
from tqdm import tqdm

def scan_port(target_ip, port, protocol="tcp"):
    """
    Función para escanear un puerto específico en una dirección IP con un protocolo dado.

    Parámetros:
    target_ip (str): La dirección IP del objetivo.
    port (int): El puerto a escanear.
    protocol (str): El protocolo a utilizar (tcp o udp). Por defecto es tcp.

    Retorna:
    (int, bool): El puerto y un booleano indicando si está abierto (True) o cerrado (False).
    """
    try:
        # Crear un socket dependiendo del protocolo
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == "tcp" else socket.SOCK_DGRAM)
        s.settimeout(0.1)  # Establecer un tiempo de espera de 0.1 segundos
        
        # Intentar conectar o enviar datos dependiendo del protocolo
        if protocol == "tcp":
            s.connect((target_ip, port))
        else:
            s.sendto(b'', (target_ip, port))
        
        s.close()  # Cerrar la conexión después de verificar el puerto

        # Intentar conectar de nuevo para confirmar
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == "tcp" else socket.SOCK_DGRAM)
        s.settimeout(0.1)
        if protocol == "tcp":
            s.connect((target_ip, port))
        else:
            s.sendto(b'', (target_ip, port))
        s.close()
        
        return port, True  # Devolver el puerto abierto
    
    except (socket.error, socket.timeout):
        return port, False  # Devolver el puerto cerrado

# Solicitar al usuario ingresar la dirección IP         
targetIP = str(input("Ingresa la dirección IP: "))

# Solicitar al usuario ingresar los puertos a escanear
startPort = int(input("Ingresa el puerto inicial del rango a escanear: "))
endPort = int(input("Ingresa el puerto final del rango a escanear: "))

# Escanear los puertos y mostrar la barra de progreso
openTCPPorts = []
openUDPPorts = []
total_ports = (endPort - startPort + 1) * 2  # El doble de puertos debido a los dos protocolos

with tqdm(total=total_ports, desc="Escaneando puertos") as pbar:
    for port in range(startPort, endPort + 1):  # Ciclo for para el escaneo de puertos
        port, is_open = scan_port(targetIP, port, protocol="tcp")
        if is_open:
            openTCPPorts.append(port)
        pbar.update(1)  # Actualizar la barra de progreso

        port, is_open = scan_port(targetIP, port, protocol="udp")
        if is_open:
            openUDPPorts.append(port)
        pbar.update(1)  # Actualizar la barra de progreso

# Guardar los puertos abiertos en un archivo
with open("puertos_abiertos.txt", "w") as file:
    if openTCPPorts:
        file.write("\nPuertos TCP abiertos:\n")
        for port in openTCPPorts:
            file.write(f"Puerto {port} (TCP) está abierto\n")
    else:
        file.write("No se encontraron puertos TCP abiertos.\n")

    if openUDPPorts:
        file.write("\nPuertos UDP abiertos:\n")
        for port in openUDPPorts:
            file.write(f"Puerto {port} (UDP) está abierto\n")
    else:
        file.write("No se encontraron puertos UDP abiertos.\n")

# Mostrar el informe de los puertos abiertos
print("\nPuertos TCP abiertos: ")
if openTCPPorts:
    for port in openTCPPorts:
        print(f"Puerto {port} (TCP) está abierto")
else:
    print("No se encontraron puertos TCP abiertos.")

print("\nPuertos UDP abiertos: ")
if openUDPPorts:
    for port in openUDPPorts:
        print(f"Puerto {port} (UDP) está abierto")
else:
    print("No se encontraron puertos UDP abiertos.")

print(f"Se encontraron {len(openTCPPorts)} puertos TCP abiertos y {len(openUDPPorts)} puertos UDP abiertos en la dirección IP {targetIP}")
print("Escaneo finalizado")  # Informar que el escaneo ha finalizado

# Cerrar el programa
print("Presione Enter para salir...")
input()  # Esperar a que el usuario presione Enter para salir
print("Saliendo...")  # Informar que se está saliendo
print("Adiós!")  # Despedirse del usuario
