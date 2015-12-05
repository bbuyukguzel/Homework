__author__ = 'Batuhan Buyukguzel'
# Python 3.5 ile test edilmistir
# Catch edemedigim bazi durumlar olmus olabilir.
# Ancak test ettigim kadariyla sorunsuz olarak calisiyor
# gibi gozukuyor hocam

import os
import subprocess
import re


def magic_trick(loc):

    try:
        list = subprocess.Popen('ls -lrt %s' % loc , shell=True,  stdout=subprocess.PIPE)
        oldest_file_line = list.stdout.readlines()[1]       # second line in the list
        oldest_file_line = oldest_file_line.decode("utf-8") # bytes object to string


        # ls -lrt command shows list of files that ordered by date (oldest to newest)
        # For example:
        #
        # b'dr-x------ 1 artyom users      4096 Oct 24 16:36 Brooklyn.Nine-Nine.S03E03.HDTV.x264-FUM[ettv]\n'
        # b'-r-------- 2 artyom users 689963008 Oct 25 00:20 archlinux-2015.10.01-dual.iso\n'
        # b'-r-------- 1 artyom users       282 Oct 25 09:58 desktop.ini\n'
        #
        # So, this a regex finds time (hh:mm format) and afterwards filename. For example:
        # 11:06 Ninite Chrome Java 8 Skype Spotify Installer.exe
        regex = re.compile('(([01]\d|2[0-3]):([0-5]\d)|24:00).*')
        oldest_file = re.search(regex, oldest_file_line).group(0)

        # Time format, has 5 letter. (e.g 11:06)
        # If i slice index 6 (including space) to end, i can accomplish the solution
        outp.write(loc+oldest_file[6:]+'\n')
    except:
        print(loc+" dizininde dosya bulunamadi")


inp = open('input.txt', 'r')    # open file for read
outp = open('output.txt', 'w')  # open file for write

for line in inp:
    try:
        # newline karakteri sorun cikartiyor.
        # bu nedenle 2 karakter kesmek durumunda kaldim
        if(os.path.isdir(line[:-2])):
            magic_trick(line[:-1])
        else:
            print('Bu konum bir dizin degil')
    except IndexError:
        print("Bu dizinde dosya bulunamadi")


inp.close()
outp.close()

