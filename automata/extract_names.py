__author__ = 'bbuyukguzel'
# Python 3.5 ile test edilmistir

import re

# bu pattern, rakam dizisini ve ardindan gelen /t yi secmeye yariyor
# ornegin test inputundan "121101021 \t" u seciyor.
# sonucu dosyaya yazarken 3 karakter eksik yaziyor cunku
# 1 karakter bosluk, 2 karakter de "\t" icin
pattern = r'^\d*(.\\t)|$'

inp = open('input.txt', 'r')    # open file for read
outp = open('output.txt', 'w')  # open file for write

for line in inp:
    match = re.search(pattern, line)
    outp.write(match.group()[:-3]+'\n')

inp.close()
outp.close()


# input.txt
"""
121101021 \t Jeyhun Karimov \t Bilgisayar Muhendisligi \t 5 \jkarimov@etu.edu.tr \t Evet \t Onayli
121021 \t Karimov \t Makina Muhendisligi \t 5 \karimov@etu.edu.tr \t Evet \t Onayli
121101021 \t AHMET GÖKHAN ŞENER \t Bilgisayar Mühendisliği \t 2 \agsener@etu.edu.tr \t Evet \t Onaylı
11110500634 \t ALPER SARIDOĞAN \t Bilgisayar Mühendisliği \t 2 \st111105006@etu.edu.tr \t Evet \t Onaylı
131101034 \t ARDA GÖKTÜRK EYÜBOĞLU \t Bilgisayar Mühendisliği \t 2 \aeyuboglu@etu.edu.tr \t Evet \t Onaylı
12110104 \t AŞKIM AKDAĞ \t Bilgisayar Mühendisliği \t 2 \aakdag@etu.edu.tr \t Evet \t Onaylı
1311020 \t AYBERK AHMET \t Bilgisayar Mühendisliği \t 2 \aahmet@etu.edu.tr \t Evet \t Onaylı
"""

# output.txt
"""
121101021
121021
121101021
11110500634
131101034
12110104
1311020
"""

