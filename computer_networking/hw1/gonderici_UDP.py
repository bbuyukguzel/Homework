import socket
import datetime


class gonderici_UDP:
    def __init__(self):
        self.filePath = ''           # Gonderilecek dosyanin konumu
        self.fileName = 'bm02_2.pdf' # Gonderilecek dosyanin adi
        self.port = 17643
        self.host = ''
        self.buffer = 2048
        # UDP icin socket olusturuluyor
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.host, self.port))

    def run(self):
        while True:
            msg, addr = self.s.recvfrom(self.buffer)
            if (msg == b'zamandamgasi'):
                self.s.sendto(datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y').encode('utf-8'), addr)
            else:
                self.s.sendto(self.fileName.encode('utf-8'), addr)
                file = open(self.filePath + self.fileName, 'rb')
#               data = file.read(self.buffer)

                i = 1
                package = (str(i) + '$').encode('utf-8')
                data = file.read(self.buffer - len(package))
                while (data):
                    if (self.s.sendto(package + data, addr)):
                        print('{0}. paket yollandi!	({1})'.format(i, len(package + data)))
                        i += 1
                        package = (str(i) + '$').encode('utf-8')
                        data = file.read(self.buffer - len(package))

                file.close()
                self.s.sendto('done'.encode('utf-8'), addr)
                print('*****    GONDERME    ISLEMI    TAMAMLANDI    *****')
        self.s.close()


g = gonderici_UDP()
g.run()
