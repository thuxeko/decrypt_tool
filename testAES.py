import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import io
import qrcode

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

qr = qrcode.QRCode(box_size=5, version=1)
test = AESCipher('Thunh@123#@!')
en_crypt = test.encrypt('dizzy coil anger fold drive echo market master boring child effort')

qr.add_data('dizzy coil anger fold drive echo market master boring child effort')
f = io.StringIO()
qr.print_ascii(out=f)
f.seek(0)
print(f.read())
# print(en_crypt.decode("utf-8"))

# print(test.decrypt(en_out))