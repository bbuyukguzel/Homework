import socket
import sys


class gonderici_UDP:
    def __init__(self):
        """
        Buffer boyutu, bilincli olarak alici tarafindaki buffer boyutundan kucuk
        secilmistir. Bunun nedeni, dosyadan okunan verinin basina eklenen header
        bilgisidir. Gonderilen paketin offseti ve checksum bilgisi dinamik oldugundan
        (ozellikle offset bilgisinin yuksek basamaklara kadar cikabileceginden)
        2000 olan bu sabit degeri uygun gorduk.
        """
        self.filePath = ''
        self.fileName = 'Data_Algorithms.pdf'
        self.PORT = 17643
        self.host = ''
        self.BUFFER = 2000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.host, self.PORT))
        self.pkt_number = 0
        self.pkt_sent = 0


    def waitACK(self):
        """
        4 farkli ACK durumu belirlendi:
        1 = OK (Packet basarili bir sekilde alindi)
        2 = Packet Corrupted (Alinan packet gonderilen ile ayni degil)
        3 = Packet Wrong Order (Packet dogru sirada alinmadi)
        None = Timeout (2 farkli durum mevcut olabilir. Ya alici taraf
                    packeti belirlenen timeout degeri icerisinde almamistir,
                    ya da alici tarafin gonderdigi ack bilgisi kaybolmus/
                    gecikmistir. Bu nedenle de cagrilan fonksiyona None bilgisi
                    gonderilir.)

        :return: ACK state
        """
        try:
            return self.s.recvfrom(self.BUFFER)[0].decode()
        except socket.timeout:
            return None

    def prepareToSend(self, i, checksum, data, addr):
        """

        :param i:
        :param checksum: Alicinin gelen bilgiyi dogrulayabilmesi icin gereken
                         checksum bilgisi
        :param data:     Aliciya gonderilecek olan veri
        :param addr:     Verinin gonderilecegi adres
        :return:         sendto fonksiyonu, kac byte'lik veri gonderildigi bilgisini
                         doner. Bu bilgi de sendFile fonksiyonundaki if ifadesinde
                         kullanilmasi amaciyla cagrilan fonksiyona dondurulur.
        """
        header = (str(i) + '$' + checksum + '$').encode()
        data_send = header + data
        returnVal = self.s.sendto(data_send, addr)
        print('{0}. paket yollandi!	<{1}>  -  ({2} bytes)'.format(self.pkt_sent, self.pkt_number,
                                                                   sys.getsizeof(data_send)))
        self.pkt_sent += 1
        ack = self.waitACK()

        if (ack == '1'):
            self.pkt_number += 1
            return returnVal
        elif (ack == '2' or ack=='3' or ack == None):
            print('Packet tekrar gonderiliyor', ack)
            return self.prepareToSend(i, checksum, data, addr)


    def sendFileName(self, addr):
        """
        Dosya adi aliciya iletilir
        :param addr: Verinin gonderilecegi adres
        """
        fileName = bytearray(self.fileName.encode())
        self.prepareToSend(self.pkt_number, str(sum(fileName)), fileName, addr)


    def sendFile(self, addr):
        """
        Belirlenen dosya aliciya iletilir
        :param addr: Verinin gonderilecegi adres
        """
        file = open(self.filePath + self.fileName, 'rb')
        data = file.read(self.BUFFER)

        checksum = str(sum(data))
        while (data):
            if (self.prepareToSend(self.pkt_number, checksum, data, addr)):
                data = file.read(self.BUFFER)
                checksum = str(sum(data))
        file.close()


    def run(self):

        """
        Programin ana fonksiyonudur. Alici ile baglantinin kurulup
        dosya aktarim islemi bu fonksiyon icerisinde baslatilir.
        Sonsuz bir dongu icerisinde surekli yeni bir alici baglantisi bekler.

        Tamamlanan her aktarim sonrasinda gonderilen packet numarisi ve
        packetin offset bilgisi sifirlanir.
        """
        while True:
            try:
                msg, addr = self.s.recvfrom(self.BUFFER)
                if(msg == b'Start'):
                    self.s.settimeout(2.0)
                    self.sendFileName(addr)
                    self.sendFile(addr)

                    self.prepareToSend(self.pkt_number, str(sum('DONE'.encode())), bytearray('DONE'.encode()), addr)
                    print('*****    GONDERME    ISLEMI    TAMAMLANDI    *****')
                    self.s.settimeout(None)
            except ConnectionResetError:
                print('Alici taraf baglantiyi kesti')
            self.s.settimeout(None)
            self.pkt_sent = 0
            self.pkt_number = 0
        self.s.close()


g = gonderici_UDP()
g.run()
