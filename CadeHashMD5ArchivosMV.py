# CadeHashMD5ArchivosMV.py
import socket
import struct
import os
import hashlib # Para calcular el hash MD5 de los archivos
HOST = "0.0.0.0"  # Dirección IP para escuchar. 0.0.0.0 significa que aceptará conexiones desde cualquier IP.
PORT = 4444
BUFFER_SIZE = 64 * 1024

def calculate_md5_from_path(file_path):
    # Se crea un objeto hash usando el algoritmo MD5.
    hasher = hashlib.md5()
    try:
        # Se abre el archivo en modo de lectura binaria ('rb'). Es importante que sea binario.
        with open(file_path, 'rb') as f:
            # Bucle que lee el archivo trozo por trozo hasta el final.
            while chunk := f.read(BUFFER_SIZE):
                # Se actualiza el objeto hash con el trozo de archivo leído.
                hasher.update(chunk)
        # Se devuelve el hash en formato hexadecimal (una cadena de texto).
        return hasher.hexdigest()
    except FileNotFoundError:
        # Si el archivo no se encuentra, la función devuelve None.
        return None

def main():
    # Se crea el socket del servidor.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Esta opción permite reutilizar la dirección y el puerto inmediatamente después de cerrar el servidor.
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Se asocia el socket a la dirección IP y puerto definidos.
        sock.bind((HOST, PORT))
        # Se pone el servidor en modo de escucha, listo para aceptar una conexión.
        sock.listen(1)
        print(f"Servidor listo y escuchando en {HOST}:{PORT}")
        print("Esperando una conexión del cliente...")

        # Bucle principal infinito para que el servidor siempre esté activo.
        while True:
            # Esta línea bloquea la ejecución hasta que un cliente se conecta.

            conn, addr = sock.accept()
            print(f"\nConexión establecida desde: {addr}")
            
            # Se usa un bloque try/finally para asegurar que la conexión se cierre al final.
            try:
                # 1. Se pide la ruta del archivo del servidor DESPUÉS de que el cliente se ha conectado.
                server_file_path = input("CLIENTE CONECTADO - Introduce la ruta del archivo de referencia (Servidor): ").strip()
                if not os.path.isfile(server_file_path):
                    print("El archivo no existe. Enviando error al cliente.")
                    conn.sendall(b"ERROR_SERVER: El archivo especificado en el servidor no fue encontrado.")
                    continue # Salta al inicio del bucle para esperar a otro cliente.

                # 2. Se envía una señal al cliente para indicarle que el servidor está listo.
                conn.sendall(b"READY")

                # 3. Se recibe primero el tamaño del archivo que enviará el cliente (8 bytes).
                file_size_bytes = conn.recv(8)
                file_size = struct.unpack("!Q", file_size_bytes)[0] # Se desempaqueta el número.

                # 4. Se reciben los datos del archivo del cliente y se calcula su hash al mismo tiempo.
                client_hasher = hashlib.md5()
                received = 0
                while received < file_size:
                    chunk = conn.recv(min(BUFFER_SIZE, file_size - received))
                    if not chunk: break # Si no se reciben más datos, se rompe el bucle.
                    client_hasher.update(chunk)
                    received += len(chunk)
                
                client_hash = client_hasher.hexdigest()

                # 5. Se calcula el hash del archivo que el usuario del servidor especificó.
                server_hash = calculate_md5_from_path(server_file_path)

                # 6. Se comparan los hashes y se envía el resultado final al cliente.
                if client_hash == server_hash:
                    conn.sendall(b"MATCH: Los archivos son identicos.")
                else:
                    conn.sendall(b"NO_MATCH: Los archivos son diferentes.")

            except Exception as e:
                print(f"Error durante la comunicación: {e}")
            finally:
                # Se asegura de que la conexión con el cliente actual siempre se cierre.
                conn.close()
                print("Conexión cerrada. Esperando un nuevo cliente...\n")

if __name__ == "__main__":
    main()