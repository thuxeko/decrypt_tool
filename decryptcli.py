from libs.aes import AESCipher
from getpass import getpass
import pyperclip


def menuRun():
    action = int(
        input('Vui long chon chuc nang: 1-Encrypt(Ma Hoa) | 2-Decrypt(Giai ma): '))
    if action in (1, 2):
        passPhrase = getpass('Vui long nhap passphrase: ')
        input_data = input('Vui long nhap chuoi can ma hoa/giai ma: ')
        actionRun(action, passPhrase, input_data)
    else:
        exit()


def actionRun(action, passPhrase, data):
    aes_cipher = AESCipher(passPhrase)
    if action == 1:  # Ma Hoa
        data_encrypt = aes_cipher.encrypt(data)
        print('Du lieu duoc ma hoa: {}'.format(data_encrypt.decode("utf-8")))
        pyperclip.copy(data_encrypt.decode("utf-8"))
    else:  # Giai ma
        data_decrypt = aes_cipher.decrypt(data)
        print('Du lieu duoc giai ma: {}'.format(data_decrypt))
        pyperclip.copy(data_decrypt)

    print('Du lieu da duoc tu dong copy vao clipboard')
    backMenu = input(
        'Nhap 1 de quay lai menu chinh hoac 0 de thoat chuong trinh')
    if backMenu == 1:
        menuRun()
    else:
        exit()


menuRun()
