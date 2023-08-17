import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import logging

logging.basicConfig(filename="log_encrypt.log",
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)

class AESService(object):
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        try:
            raw = self._pad(raw)
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode("utf-8")
        except Exception as e:
            logging.error(e)
            return 'Error Encrypt {}'.format(e)

    def decrypt(self, enc):
        try:
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        except Exception as e:
            logging.error(e)
            return 'Error Decrypt {}'.format(e)

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]