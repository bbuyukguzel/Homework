__author__ = 'Batuhan BUYUKGUZEL'


import re
import sys

#\b\d{2}/\d{2}/\d{2}\b

def change_format(string):
    # beta list contains both datetime format (dd-mm-20yy) and other formats which
    # we don't want to change this kind of strings (3/234/12). I used beta list
    # to swap strings.
    beta = []
    # alpha list contains strings which are proper d/d/d format (or d*/d*/d*)
    alpha = re.findall(r'(\d*[0-9][0-9]/[0-9][0-9]/[0-9][0-9]\d*)', string)
    for i in alpha:
        # If element i larger than 8 length, this string shouldn't be changed.
        # It probably seems to 123/1233/1256 format.
        if len(i) <= 8:
            beta.append(i[3:5]+"-"+i[0:2]+"-20"+i[6:8])
        else:
            beta.append(i)
    # elements swap in this loop
    for i in range(0, len(alpha)):
        string = string.replace(alpha[i], beta[i])
    return string


file_name = sys.argv[1]
read_me = open(file_name, "r")
write_me = open(file_name.split('.')[0]+"-modified.txt", "w")

for line in read_me:
    write_me.write(change_format(line))

read_me.close()
write_me.close()