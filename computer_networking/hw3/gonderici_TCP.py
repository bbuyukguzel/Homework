import socket
import ssl
import OpenSSL
from Crypto.PublicKey import RSA
from Crypto.Util import asn1


class gonderici_TCP:
    def __init__(self):
        self.filePath = ''
        self.fileName = 'Data_Algorithms.pdf'
        self.port = 17642
        self.buffer = 2048
        self.s = None
        self.ssl_socket = None
        self.DEBUG = True
        self.context = None

    def setup(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.load_cert_chain(certfile='server.pem', keyfile='server.key')
        self.context.load_verify_locations(cafile='ca.pem')
        self.context.set_ciphers('ECDH+AESGCM')

        self.ssl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ssl_socket.bind(('', self.port))
        self.ssl_socket.listen(5)

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
        while True:
            try:
                newsocket, fromaddr = self.ssl_socket.accept()
                connstream = self.context.wrap_socket(newsocket, server_side=True)
                cert = connstream.getpeercert(binary_form=True)
                pem = ssl.DER_cert_to_PEM_cert(cert)
                self.getPublicKey(pem)

                # Ilk olarak dosyanin adi gonderilir
                connstream.send(self.fileName.encode('utf-8'))
                # Gonderilecek dosya, 'read binary' parametresiyle acilir
                file = open(self.filePath + self.fileName, 'rb')
                # Dosyadan buffer boyutu kadar byte okunur
                data = file.read(self.buffer)
                # Okunan byte'lar karsi tarafa gonderilir
                connstream.send(data)

                # Okunan 'data' bos olmadigi surece dongu calisir
                # Donguye her giriste dosyadan buffer boyutunda veri
                # okunur ve karsi tarafi gonderilir.
                while (data):
                    data = file.read(self.buffer)
                    # ssl.SSLEOFError: EOF occurred in violation of protocol
                    # hatasinin cozumu icin 'dirty solution'
                    if(data): connstream.send(data)

                connstream.send(b'DONE')
                # Aktarim tamamlandi. Dosya kapatilir.
                file.close()
                print('*****    GONDERME    ISLEMI    TAMAMLANDI    *****\n\n')
            except Exception as err:
                print(err)
        self.ssl_socket.close()


print('fra1-01 IP: 46.101.202.226\n'
      'fra1-02 IP: 46.101.222.96')
g = gonderici_TCP()
g.setup()
g.run()