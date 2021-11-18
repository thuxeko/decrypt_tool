import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import *

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

# Image class for QR code
class Image(qrcode.image.base.BaseImage):
  
    # constructor
    def __init__(self, border, width, box_size):
  
        # assigning border
        self.border = border
  
        # assigning  width
        self.width = width
  
        # assigning box size
        self.box_size = box_size
  
        # creating size
        size = (width + border * 2) * box_size
  
        # image
        self._image = QImage(size, size, QImage.Format_RGB16)
  
        # initial image as white
        self._image.fill(Qt.white)
  
  
    # pixmap method
    def pixmap(self):
  
        # returns image
        return QPixmap.fromImage(self._image)
  
    # drawrect method for drawing rectangle
    def drawrect(self, row, col):
  
        # creating painter object
        painter = QPainter(self._image)
  
        # drawing rectangle
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            QtCore.Qt.black)

class QrWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code")
        layout = QVBoxLayout()
        self.label = QLabel(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def displayInfo(self):
        self.show()         

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        fileh = QtCore.QFile('aestools.ui')
        fileh.open(QtCore.QFile.ReadOnly)
        loadUi(fileh, self)
        self.setFixedSize(320, 290)
        self.qrWindow = QrWindow()
        # btn action
        self.btnShowHide.clicked.connect(self.toggleVisibility)
        self.btnEncrypt.clicked.connect(self.encryptAction)
        self.btnDecrypt.clicked.connect(self.decryptAction)
        self.btnShowQr.clicked.connect(self.showQr)
    
    def toggleVisibility(self):
        if self.txtPassphrase.echoMode()==QLineEdit.Normal:
            self.txtPassphrase.setEchoMode(QLineEdit.Password)
        else:
            self.txtPassphrase.setEchoMode(QLineEdit.Normal)

    def encryptAction(self):
        passPhrase = self.txtPassphrase.text()
        inputText = self.txtInput.toPlainText()
        aesCipher = AESCipher(passPhrase)

        encryptSuccess = aesCipher.encrypt(inputText)
        self.txtOutput.setPlainText(encryptSuccess.decode("utf-8"))

    def decryptAction(self):
        passPhrase = self.txtPassphrase.text()
        inputText = self.txtInput.toPlainText()
        aesCipher = AESCipher(passPhrase)

        decryptSuccess = aesCipher.decrypt(inputText)
        self.txtOutput.setPlainText(decryptSuccess)

    def showQr(self):
        decryptSuccess = self.txtOutput.toPlainText()
        qr_image = qrcode.make(decryptSuccess, image_factory = Image).pixmap()
        self.qrWindow.label.setPixmap(qr_image)
        self.qrWindow.displayInfo()
# main
app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec_())