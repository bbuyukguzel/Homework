__author__ = 'Batuhan Buyukguzel'


n = int(input('N degerini giriniz: '))
print('\nTimes: ', end='')

row = 1
col = 1

# ekrana basilacak toplam deger sayisi = n^2+2n
# ornegin:
# n=1 => 3,  n=2 => 8
# n=3 => 15, n=4 => 24 ...
for i in range(1, (n**2)+(2*n)+1):

    # n degerine ulastiginda alt satira gec
    if(col==n+1):
        print()
        row = i%n

        # son satira geldiginde row'un 0 olmamasi icin
        # bir kontrol ifadesi orn: 9%9=0
        if(i%n==0):
            row = n

        # Yeni satira her gecildiginde satir numarasinin
        # (1...n) ekrana yazdirilmasi
        print(end=str(row).ljust(7, ' '))
        col = 1
        continue

    # Carpim sonucunun ekrana yazdirilmasi
    print(end=str(row*col).ljust(6, ' '))
    col = col + 1




