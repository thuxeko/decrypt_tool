import base64
import hashlib
import sys
from Cryptodome.Cipher import AES
from Cryptodome import Random
import logging

logging.basicConfig(filename="log_encrypt.log",
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)

class AESCipher:
    BLOCK_SIZE = 16
    KEY_LEN = 32
    IV_LEN = 16

    def __init__(self):
        self.py2 = sys.version_info[0] == 2

    def encrypt(self, raw, passphrase):
        salt = Random.new().read(8)
        key, iv = self.__derive_key_and_iv(passphrase, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(b'Salted__' + salt + cipher.encrypt(self.__pkcs7_padding(raw))).decode("utf-8")

    def decrypt(self, enc, passphrase):
        ct = base64.b64decode(enc)
        salted = ct[:8]
        if salted != b'Salted__':
            return ""
        salt = ct[8:16]
        key, iv = self.__derive_key_and_iv(passphrase, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return self.__pkcs7_trimming(cipher.decrypt(ct[16:])).decode("utf-8")

    def __pkcs7_padding(self, s):
        s_len = len(s if self.py2 else s.encode('utf-8'))
        s = s + (self.BLOCK_SIZE - s_len % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - s_len % self.BLOCK_SIZE)
        return s if self.py2 else bytes(s, 'utf-8')

    def __pkcs7_trimming(self, s):
        if sys.version_info[0] == 2:
            return s[0:-ord(s[-1])]
        return s[0:-s[-1]]

    def __derive_key_and_iv(self, password, salt):
        d = d_i = b''
        enc_pass = password if self.py2 else password.encode('utf-8')
        while len(d) < self.KEY_LEN + self.IV_LEN:
            d_i = hashlib.md5(d_i + enc_pass + salt).digest()
            d += d_i
        return d[:self.KEY_LEN], d[self.KEY_LEN:self.KEY_LEN + self.IV_LEN]
