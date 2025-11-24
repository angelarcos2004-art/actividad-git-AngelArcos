import hashlib

def generate_md5_hash(text):

    # Create an MDS object
    md5_obj = hashlib.md5()
    
    # Add the text to the MDS object
    md5_obj.update(text.encode())
    
    # Get the hexadecimal digest of the hash
    hash_value = md5_obj.hexdigest()
    
    # Return the hash value
    return hash_value

# Test the function
if __name__ == "__main__":

    text = "Hello, world!"
    mensaje = "Hello, world!"
    hashT1 = generate_md5_hash(text)
    hashT2 = generate_md5_hash(mensaje)
    
    # Compara los hashes y muestra el resultado
    print("Las cadenas generadas son iguales?, ", hashT1 == hashT2)
    print("Clave Hash1:", hashT1)
    print("Clave Hash2:", hashT2)
    