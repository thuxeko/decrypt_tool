import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from libs.aesService import AESService
from libs.rsaService import RSAService
from libs.aesCipher import AESCipher

import logging
import os
import json
import qrcode

logging.basicConfig(filename="log_encrypt.log",
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)

config_name = 'rsaconfig.json'
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, config_name)
with open(config_path) as json_file:
    rsaConfig = json.load(json_file)

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
        fileh = QtCore.QFile('encrypttool.ui')
        fileh.open(QtCore.QFile.ReadOnly)
        loadUi(fileh, self)
        self.setFixedSize(320, 320)
        self.qrWindow = QrWindow()

        # btn action
        self.btnShowHide.clicked.connect(self.toggleVisibility)
        self.btnEncrypt.clicked.connect(self.encryptAction)
        self.btnDecrypt.clicked.connect(self.decryptAction)
        self.btnShowQr.clicked.connect(self.showQr)

        # radio
        self.rbAES.clicked.connect(self.uiCheck)
        self.rbRSA.clicked.connect(self.uiCheck)

    def uiCheck(self):
        if self.rbAES.isChecked():
            self.txtPassphrase.setEnabled(True)
            self.btnShowHide.setEnabled(True)
        elif self.rbRSA.isChecked():
            self.txtPassphrase.setEnabled(False)
            self.btnShowHide.setEnabled(False)
        self.txtPassphrase.setText("")

    def toggleVisibility(self):
        if self.txtPassphrase.echoMode() == QLineEdit.Normal:
            self.txtPassphrase.setEchoMode(QLineEdit.Password)
        else:
            self.txtPassphrase.setEchoMode(QLineEdit.Normal)

    def encryptAction(self):
        passPhrase = self.txtPassphrase.text()
        inputText = self.txtInput.toPlainText()
        if self.rbAES.isChecked():
            # aesCipher = AESService(passPhrase)
            # encryptSuccess = aesCipher.encrypt(inputText)
            
            aess = AESCipher()
            encryptSuccess = aess.encrypt(inputText, passPhrase)

            self.txtOutput.setPlainText(encryptSuccess)
            logging.info(
                'AES - Encrypt: {}'.format(encryptSuccess))
        elif self.rbRSA.isChecked():
            rsaCipher = RSAService(rsaConfig['private'], rsaConfig['public'])
            encryptSuccess = rsaCipher.encrypt(inputText)
            self.txtOutput.setPlainText(encryptSuccess)
            logging.info('RSA - Encrypt: {}'.format(encryptSuccess))

    def decryptAction(self):
        decryptSuccess = None
        passPhrase = self.txtPassphrase.text()
        inputText = self.txtInput.toPlainText()

        if self.rbAES.isChecked():
            # aesCipher = AESService(passPhrase)
            # decryptSuccess = aesCipher.decrypt(inputText)

            aess = AESCipher()
            decryptSuccess = aess.decrypt(inputText, passPhrase)
        elif self.rbRSA.isChecked():
            rsaCipher = RSAService(
                rsaConfig['private'], rsaConfig['public'])
            decryptSuccess = rsaCipher.decrypt(inputText)

        self.txtOutput.setPlainText(decryptSuccess if decryptSuccess else 'Invalid Data')

    def showQr(self):
        decryptSuccess = self.txtOutput.toPlainText()
        qr_image = qrcode.make(decryptSuccess, image_factory=Image).pixmap()
        self.qrWindow.label.setPixmap(qr_image)
        self.qrWindow.displayInfo()


# main
app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec_())
