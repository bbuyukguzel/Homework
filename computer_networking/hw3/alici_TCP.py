import socket
import ssl
import OpenSSL
from Crypto.PublicKey import RSA
from Crypto.Util import asn1


class alici_TCP:
    def __init__(self, host):
        self.host = host
        self.port = 17642
        self.buffer = 2048
        self.loc = ''
        self.s = None
        self.ssl_socket = None

    def setup(self):

        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = False
        try:
            context.load_cert_chain(certfile='client.pem', keyfile='client.key')
            context.load_verify_locations(cafile='ca.pem')
            context.set_ciphers('ECDH+AESGCM')

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ssl_socket = context.wrap_socket(self.s, server_hostname='localhost')
            self.ssl_socket.connect((self.host, 17642))

        except FileNotFoundError:
            print('certfile/certfile/cafile parametrelerinden birisi verilen dosya konumunda bulunamadi')
        except ssl.SSLError as err:
            if '[SSL] PEM lib' in err.strerror:
                print('Verilen certfile ile keyfile uyusmamaktadir')
            else:
                print(err)


    def getPublicKey(self, cert):
        # Convert PEM format to x509 Object
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        # Extract the public key
        pub_key = x509.get_pubkey()
        # Print the public key in TEXT formatboru
        pub_key_text = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_TEXT, pub_key)
        # Convert to ASN1
        pub_key_asn1 = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, pub_key)
        # Convert key to DER format
        pub_der = asn1.DerSequence()
        pub_der.decode(pub_key_asn1)
        # Construct RSA key
        # In Python 3 you no longer use "long" -> Use "int" instead
        b = RSA.construct((int(pub_der._seq[1]), int(pub_der._seq[2])))
        # Print public key information
        print(pub_key_text.decode("utf-8"), end='')
        print('- Certificate  Type ‐\nX.509\n')

    def run(self):
        cert = self.ssl_socket.getpeercert(binary_form=True)
        pem = ssl.DER_cert_to_PEM_cert(cert)
        self.getPublicKey(pem)

        fileName = self.ssl_socket.recv(self.buffer).decode('utf-8')
        fname, extension = fileName.split('.')
        # Alinan dosya adinin sonuna 'alindi' eklenir
        fileName = fname + '_alindi.' + extension
        # Dosya, yeni adiyla 'write binary' parametresiyle acilir.
        f = open(self.loc + fileName, 'wb')

        # Karsidan gelen mesaj okunur
        l = self.ssl_socket.recv(self.buffer)
        # Mesaj bos olmadigi surece dongu calisir.
        # Okunan bilgi dosyaya yazilir, ve karsidan yeni mesaj okunur.
        while (l):
            f.write(l)
            l = self.ssl_socket.recv(self.buffer)
            if(l==b'DONE'): break

        f.write(b'')
        # Dosya alma islemi tamamlandi. Dosya kapatilir.
        f.close()
        print('*****    ALMA    ISLEMI    TAMAMLANDI    *****')
        self.ssl_socket.close()



print('fra1-01 IP: 46.101.202.226\n'
      'fra1-02 IP: 46.101.222.96')
host = input('Gonderici sunucunun IP\'sini giriniz: ')
alici = alici_TCP(host)
alici.setup()
alici.run()
