import socket
import datetime


class gonderici_TCP:
    def __init__(self):
        self.filePath = ''           # Gonderilecek dosyanin konumu
        self.fileName = 'bm02_2.pdf' # Gonderilecek dosyanin adi
        self.port = 17642
        self.buffer = 2048

        # TCP icin socket olusturuluyor
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Host ve port bilgisi binding yapilir.
        self.s.bind(('', self.port))

        # 1 baglanti icin dinlenmeye baslanir
        self.s.listen(1)

    def run(self):
        while True:
            # Baglanti bekleniyor
            connect, address = self.s.accept()
#           print('{} baglandi'.format(address))

            # Bir mesaj bilgisi bekleniyor
            msg = connect.recv(self.buffer).decode("utf-8")
            # 'zamandamgasi' geldiyse, karsi tarafa timestamp bilgisi gonderilir
            if (msg == 'zamandamgasi'):
                connect.send(datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y').encode('utf-8'))
            # 'zamandamgasi' degilse, onceden belirlenen dosya karsi tarafa gonderilir
            else:
                # Ilk olarak dosyanin adi gonderilir
                connect.send(self.fileName.encode('utf-8'))
                # Gonderilecek dosya, 'read binary' parametresiyle acilir
                file = open(self.filePath + self.fileName, 'rb')
                # Dosyadan buffer boyutu kadar byte okunur
                data = file.read(self.buffer)
                # Okunan byte'lar karsi tarafa gonderilir
                connect.send(data)

                # Okunan 'data' bos olmadigi surece dongu calisir
                # Donguye her giriste dosyadan buffer boyutunda veri
                # okunur ve karsi tarafi gonderilir.
                while (data):
                    data = file.read(self.buffer)
                    connect.send(data)

                # Aktarim tamamlandi. Dosya kapatilir.
                file.close()
                print('*****    GONDERME    ISLEMI    TAMAMLANDI    *****')
            # Baglanti kapatilir.
            connect.close()


g = gonderici_TCP()
g.run()
