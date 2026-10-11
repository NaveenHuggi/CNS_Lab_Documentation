from Crypto.Cipher import DES
from Crypto.Util.Padding import pad,unpad

key=b"12345678"
cipher=DES.new(key,DES.MODE_ECB)
pt=input("Enter Message: ")
ct=cipher.encrypt(pad(pt.encode(),DES.block_size))
print("Encrypted:",ct.hex())
print("Decrypted:",unpad(cipher.decrypt(ct),DES.block_size).decode())
