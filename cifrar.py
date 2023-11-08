import hashlib
contrasena = input("Digite su contraseña: ")
cifrada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()
print(cifrada)