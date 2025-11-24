import hashlib

def calculate_md5(file_path):

    hasher = hashlib.md5()
    
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(8192)
                if not data:
                    break
                hasher.update(data)
        
        return hasher.hexdigest()

    except FileNotFoundError:
        print(f"Error: El archivo en la ruta '{file_path}' no fue encontrado.")
        return None

if __name__ == "__main__":
    
    file_path1 = input("Introduce la ruta del archivo número 1: ")
    md5_hash1 = calculate_md5(file_path1)

    file_path2 = input("Introduce la ruta del archivo número 2: ")
    md5_hash2 = calculate_md5(file_path2)

    if md5_hash1 and md5_hash2:
        print(f"Hash MD5 Archivo 1: {md5_hash1}")
        print(f"Hash MD5 Archivo 2: {md5_hash2}")

        if md5_hash1 == md5_hash2:
            print("\nLos archivos son idénticos")
        else:
            print("\nLos archivos son diferentes")