# -*- coding: utf-8 -*-
__author__ = 'bbuyukguzel'

alfabe = {'a': 0, 'b': 1, 'c': 2, 'ç': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'ğ': 8, 'h': 9, 'ı': 10, 'i': 11, 'j': 12, 'k': 13, 'l': 14, 'm': 15, 'n': 16, 'o':
17, 'ö': 18, 'p': 19, 'r': 20, 's': 21, 'ş': 22, 't': 23, 'u': 24, 'ü': 25, 'v': 26, 'y': 27, 'z': 28 }

alfabe_ters = dict([[v,k] for k,v in alfabe.items()])
alfabe_büyüklük = 29
metin = input('şifrelenecek metini giriniz: ')
şifreli_metin = '' # şifreli metin başlangıçta boş
anahtar = input('anahtarı giriniz: ')


# anahtar uzunlugu metin uzunluguna gelecek sekilde genisletilecek.
# ornegin metin 12 karakter ve key=lemon olsun.
# bu islemin ardindan key=lemonlemonle olacaktir.
sum = len(metin)//len(anahtar) # floor division
carry = len(metin)%len(anahtar)# modulus
cycle_key = (anahtar*sum)+(anahtar[:carry])


check = True
for i in anahtar:              # anahtardaki bir karakter alfabede yok ise
    if not i in alfabe.keys(): # hatali key girdiniz uyarisi ver.
        check = False

# Ornegin key @ iceriyorsa uyari ver.
if(check):
    for i in range(0, len(metin)):
        if metin[i] in alfabe.keys():
            m = alfabe[metin[i]]       # metindeki i inci karakterin degeri
            k = alfabe[cycle_key[i]]   # anahtardaki i inci karakterin degeri
            c = (m+k)%alfabe_büyüklük  # m ve k toplaminin mod 29'daki degeri
            şifreli_metin = şifreli_metin + alfabe_ters[c]
        else:
            şifreli_metin+=metin[i] # alfabede olmayan karakterleri olduğu gibi bırakmak için
            # alfabede olmayan karakterleri olduğu gibi bırakmak için
    print('şifrelenmiş metin: ', şifreli_metin)
else:
    print('hatalı anahtar girdiniz')
