import socket
import datetime


class alici_TCP:
    def __init__(self, host):
        self.host = host
        self.port = 17642
        self.buffer = 2048
        self.loc = ''       # Alinacak dosyanin konumu
        self.s = socket.socket()
        self.s.connect((host, self.port))

    def run(self):
        # Karsi tarafa gonderilecek mesaj aliniyor
        cmd = input('').encode('utf-8')
        # Alinan mesaj karsi tarafa gonderiliyor.
        self.s.send(cmd)
        # Gonderilen mesaj 'zamandamgasi' ise, karsi taraftan gelen
        # bilgi ekrana yazdirilir.
        if (cmd == b'zamandamgasi'):
            print(self.s.recv(self.buffer).decode('utf-8'))
        else:
            start = datetime.datetime.now()
            # Dosya adi karsi taraftan alinir.
            fileName = self.s.recv(self.buffer).decode('utf-8')
            fname, extension = fileName.split('.')
            # Alinan dosya adinin sonuna 'alindi' eklenir
            fileName = fname + '_alindi.' + extension
            # Dosya, yeni adiyla 'write binary' parametresiyle acilir.
            f = open(self.loc + fileName, 'wb')

            # Karsidan gelen mesaj okunur
            l = self.s.recv(self.buffer)
            # Mesaj bos olmadigi surece dongu calisir.
            # Okunan bilgi dosyaya yazilir, ve karsidan yeni mesaj okunur.
            while (l):
                f.write(l)
                l = self.s.recv(self.buffer)

            # Dosya alma islemi tamamlandi. Dosya kapatilir.
            f.close()
            end = datetime.datetime.now()
            print(end - start)
            print(int((end - start).total_seconds() * 1000))  # milliseconds)
            print('*****    ALMA    ISLEMI    TAMAMLANDI    *****')
            # Socket kapatilir.
            self.s.close


host = input('Gonderici sunucunun IP\'sini giriniz: ')
alici = alici_TCP(host)
alici.run()
