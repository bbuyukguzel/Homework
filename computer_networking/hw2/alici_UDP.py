import socket
import sys
import time
import datetime
"""
Packet loss
	sender ack alamaz (timeout)
	resend
ACK loss
	sender ack alamaz (timeout)
	resend
	duplicate detection yapılmalı
Premature timeout/delayed ACK
	sender ack alamadigindan tekrar gonderir
	receiver duplicate detection yapmalidir
"""

class alici_UDP:
    def __init__(self, host):
        self.port = 17643
        self.host = host
        self.buffer = 2048
        self.loc = ''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (self.host, self.port)
        self.prevPktNumber = -1
        self.pkt_get = 0
        self.DEBUG = True


    def isDuplicate(self, pkt_number):
        """
        Stop&Wait yontemi kullanildigindan dolayi, duplicate kontrolu icin yalnizca
        aldigimiz son packetin offset bilgisi ile gelen packetin offset bilgisini
        karsilastirmak bu is icin yeterlidir.

        :param pkt_number: Alinan packetin kacinci sirada oldugu bilgisi
        :return: Alinan packetin daha once alinip alinmadigi bilgisi
        """
        return self.prevPktNumber == int(pkt_number)


    def isWrongOrder(self, pkt_number):
        """
        Stop&Wait yontemi kullanildigindan dolayi, alicinin bekledigi packet offseti,
        son alinan packet offsetinden bir fazla olmalidir.

        :param pkt_number: Alinan packetin kacinci sirada oldugu bilgisi
        :return: Alinan packetin dogru sirada olup olmadigi bilgisi
        """
        return self.prevPktNumber+1 != int(pkt_number)


    def isDataVerified(self, checksum, data):
        """
        Alinan verinin dogru/eksiksiz olup olmadigi bilgisi bu fonksiyon ile
        elde edilir. Gelen packettaki data bilgisinin (header haricindeki kisim)
        checksum'i hesaplanir ve bu deger gelen packettaki checksum bilgisi ile
        karsilastilir.

        :param checksum: Alinan packetin headerindaki checksum bilgisi
        :param data: Alinan packettaki header haricindeki veri
        :return: Alinan packetin eksiksiz olarak gelip gelmedigi bilgisi
        """
        return checksum != str(sum(data.encode('latin-1')))


    def rcv_data(self):
        self.s.settimeout(2.0)
        self.pkt_get += 1
        try:
            pkt_number, checksum, data = (self.s.recvfrom(self.buffer)[0].decode('latin-1')).split('$', 2)
            if not self.isWrongOrder(pkt_number):                   # Packet order is true
                if not self.isDataVerified(checksum, data):         # Packet verified
                    self.s.sendto('1'.encode('utf-8'), self.addr)   # ACK: OK
                    self.prevPktNumber = int(pkt_number)
                    print('{0}. paket alindi! <{1}> (<{2} bytes>) {3}'.format(self.pkt_get, pkt_number, sys.getsizeof(data), 'KABUL(sirali)'))
                    return pkt_number, data
                else:                                               # Packet corrupted
                    print('{0}. paket alindi! <{1}> (<{2} bytes>) {3}'.format(self.pkt_get, pkt_number, sys.getsizeof(data), 'RET)'))
                    print('Packet Corrupted')
                    self.s.sendto('2'.encode('utf-8'), self.addr)   # ACK: Packet Corrupted
                    return pkt_number, '-1'
            else:
                if self.isDuplicate(pkt_number):
                    print('{0}. paket alindi! <{1}> (<{2} bytes>) {3}'.format(self.pkt_get, pkt_number, sys.getsizeof(data), 'RET'))
                    print('Packet Duplicate')
                    if (self.DEBUG): time.sleep(0.5)
                    self.s.sendto('1'.encode('utf-8'), self.addr)
                    return pkt_number, '-1'
                else:
                    print('{0}. paket alindi! <{1}> (<{2} bytes>) {3}'.format(self.pkt_get, pkt_number, sys.getsizeof(data), 'KABUL(yanlis sirada)'))
                    print('Packet Wrong Order')
                    if (self.DEBUG): time.sleep(0.5)
                    self.s.sendto('3'.encode('utf-8'), self.addr)       # ACK: Packet order is wrong
                    return pkt_number, '-1'
        except socket.timeout as err:
            # Timeout icin ACK gondermeye gerek yok. Cunku karsi tarafta zaten
            # timeout kontrolu yapiliyor. ACK gelmedigi zaman paket tekrar gonderilecek.
            #self.s.sendto('4'.encode('utf-8'), self.addr)
            if (self.DEBUG): print(err)
            print('Timeout')
            return pkt_number, '-1'
            #return 0, '-1'


    def run(self):
        self.s.sendto('Start'.encode('utf-8'), self.addr)
        start = datetime.datetime.now()
        try:
            fileName = self.rcv_data()[1]
            fname, extension = fileName.split('.')
            fileName = fname + '_alindi.' + extension
            f = open(self.loc + fileName, 'wb')

            data = (self.rcv_data()[1])
            while (data):
                f.write(data.encode('latin-1'))

                if (data == 'DONE'): break
                data = self.rcv_data()[1]
                while(data=='-1'):               # ack -1 durumunda oldugu surece tekrar data oku
                    data = self.rcv_data()[1]
                if (data == 'DONE'): break       # dosyanin sonuna 'done' eklememek icin dirty bir solution
                self.s.settimeout(8.0)

            f.close()
            end = datetime.datetime.now()
            print(int((end - start).total_seconds() * 1000))  # milliseconds)
            print('*****    ALMA    ISLEMI    TAMAMLANDI    *****')

        except UnicodeDecodeError as err:
            if (self.DEBUG): print(err)
            print('Dosya adi ile ilgili bir hata olustu')
        except socket.timeout as err:
            if (self.DEBUG): print(err)
            print('Dosya alinirken bir hata olustu (Timeout)')
        except ValueError as err:
            #print(err.with_traceback())
            if (self.DEBUG): print(err)
            print('Dosya adi parse edilirken bir hata olustu')

        self.s.close  # Close the socket when done


host = input('Gonderici sunucunun IP\'sini giriniz: ')
alici = alici_UDP(host)
alici.run()
