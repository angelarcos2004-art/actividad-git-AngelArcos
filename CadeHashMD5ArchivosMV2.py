# CadeHashMD5ArchivosMV2.py

import socket  # Para la comunicación por red
import struct  # Para empaquetar el tamaño del archivo en formato binario
import os      # Para obtener el tamaño del archivo y verificar que existe
import sys     # Para salir del programa si el archivo no se encuentra

SERVER_HOST = "100.89.250.119"
SERVER_PORT = 4444
BUFFER_SIZE = 64 * 1024

def main():
    # Se crea el socket del cliente.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            # 1. Se intenta establecer la conexión con el servidor.
            print(f"Intentando conectar con el servidor en {SERVER_HOST}:{SERVER_PORT}...")
            sock.connect((SERVER_HOST, SERVER_PORT))
            print("Conexión exitosa con el servidor.")

            # Se espera a recibir la señal "READY" del servidor. Esto sincroniza ambos programas.
            signal = sock.recv(1024)
            if signal != b"READY":
                # Si el servidor envía otra cosa (probablemente un error), se muestra y se termina.
                print(f"Error del servidor: {signal.decode()}")
                return

            # 2. Se pide la ruta del archivo local DESPUÉS de confirmar la conexión.
            local_path = input("Introduce la ruta del archivo local a verificar: ").strip()

            # Se comprueba si el archivo realmente existe antes de continuar.
            if not os.path.isfile(local_path):
                print(f"Error: Archivo no encontrado en '{local_path}'")
                return # Se cierra la conexión y termina el script.

            # Se obtiene el tamaño del archivo para enviarlo primero.
            file_size = os.path.getsize(local_path)

            # 3. Se envía el archivo al servidor para la comparación.
            print(f"Enviando '{os.path.basename(local_path)}' para su comparación...")
            # Se empaqueta el tamaño del archivo en 8 bytes y se envía.
            sock.sendall(struct.pack("!Q", file_size))
            # Se abre el archivo en modo lectura binaria ('rb').
            with open(local_path, "rb") as f:
                # Bucle para leer y enviar el archivo trozo por trozo.
                while chunk := f.read(BUFFER_SIZE):
                    sock.sendall(chunk)

            # 4. Se recibe el veredicto final del servidor.
            response = sock.recv(1024).decode()
            print("\n--- Resultado de la Comparación ---")
            print(f"Respuesta del servidor: {response}")

        except ConnectionRefusedError:
            # Este error ocurre si el servidor no está corriendo o la IP/puerto es incorrecta.
            print("Error: Conexión rechazada. Asegúrate de que el servidor esté corriendo.")
        except Exception as e:
            # Captura cualquier otro error que pueda ocurrir durante la comunicación.
            print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()