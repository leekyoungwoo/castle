import pyDes
import base64


class DES:
    def __init__(self, iv='jiran1!@', key='jiran1!@'):
        self.iv = iv
        self.key = key

    def encrypt(self, data):
        k = pyDes.des(self.key, pyDes.CBC, self.iv, padmode=pyDes.PAD_PKCS5)
        d = k.encrypt(data)
        d = base64.b32encode(d)
        return d

    def decrypt(self, data):
        k = pyDes.des(self.key, pyDes.CBC, self.iv, padmode=pyDes.PAD_PKCS5)
        data = base64.b32decode(data)
        d = k.decrypt(data).decode()
        return d


if __name__ == '__main__':
    des = DES()
    for i in range(1000,5000):
        encryptdata = des.encrypt(str(i))
        print(encryptdata.decode()[:-1])
        decryptdata = des.decrypt(encryptdata)
        print(decryptdata)
        decryptdata = des.decrypt(encryptdata.decode())
        print(decryptdata)
