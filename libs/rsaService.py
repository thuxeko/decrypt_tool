
from typing import Final
from Crypto import PublicKey
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


class RSAService():
    __PRIVATE_KEY: Final = b''
    
    __PUBLIC_KEY: Final = b''

    def __init__(self, private_key: str = None, public_key: str = None): 
        self.private_key = private_key if private_key else self.__PRIVATE_KEY
        self.public_key = public_key if public_key else self.__PUBLIC_KEY

    def encrypt(self, data: str):
        publicKey: Final = RSA.import_key(self.public_key)
        encryptor = PKCS1_OAEP.new(publicKey)
        return base64.b64encode(encryptor.encrypt(str.encode(data))).decode()
    
    def decrypt(self, data: str):
        msg = base64.b64decode(str.encode(data))
        privateKey = RSA.import_key(self.private_key)
        decryptor = PKCS1_OAEP.new(privateKey)
        return decryptor.decrypt(msg).decode('utf-8')        