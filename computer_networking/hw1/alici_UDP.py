import socket
import datetime


class alici_UDP:
    def __init__(self, host):
        self.port = 17643
        self.host = host
        self.buffer = 2048
        self.loc = ''       # Alinacak dosyanin konumu
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (self.host, self.port)

    def run(self):
        cmd = input('').encode('utf-8')
        self.s.sendto(cmd, self.addr)
        if (cmd == b'zamandamgasi'):
            print(self.s.recv(self.buffer).decode('utf-8'))
        else:
            start = datetime.datetime.now()
            try:
                fileName = self.s.recvfrom(self.buffer)[0].decode('utf-8')  # decode()
                fname, extension = fileName.split('.')
                fileName = fname + '_alindi.' + extension
                f = open(self.loc + fileName, 'wb')

                i = 0
                data, addr = self.s.recvfrom(self.buffer)
                while (data):
                    i = (data.decode('latin-1').encode("utf-8")).find(b'$')
                    f.write(data[i + 1:])
                    if (data == b'done'): break
                    print('{}. paket alindi!'.format(data[:i].decode('utf-8')))
                    data, addr = self.s.recvfrom(self.buffer)
                    self.s.settimeout(8.0)

                f.close()
                end = datetime.datetime.now()
                print(end - start)
                print(int((end - start).total_seconds() * 1000))  # milliseconds)
                print('*****    ALMA    ISLEMI    TAMAMLANDI    *****')
            except UnicodeDecodeError:
                print('Dosya adi ile ilgili bir hata olustu')
            except socket.timeout:
                print('Dosya alinirken bir hata olustu (Timeout)')
            except ValueError:
                print('Dosya adi parse edilirken bir hata olustu')
            self.s.close  # Close the socket when done


host = input('Gonderici sunucunun IP\'sini giriniz: ')
alici = alici_UDP(host)
alici.run()
