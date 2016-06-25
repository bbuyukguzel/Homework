//
// Created by roland on 06.06.2016.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sys/wait.h>


#define BASLAT 1
#define BEKLET 2
#define YURUT 3
#define DURDUR 4
#define SURDUR 5
#define OLDUR 6
#define KAPAT 7
#define HATA 9


// Switch casede kullanilmak uzere, kullanicidan alinan inputa karsilik gelen deger dondurulur.
int check_command(char *input) {
    const char *commands[7] = {"başlat", "beklet", "yürüt", "durdur", "sürdür", "öldür", "kapat"};

    if (strcmp(commands[0], input) == 0)
        return BASLAT;
    else if (strcmp(commands[1], input) == 0)
        return BEKLET;
    else if (strcmp(commands[2], input) == 0)
        return YURUT;
    else if (strcmp(commands[3], input) == 0)
        return DURDUR;
    else if (strcmp(commands[4], input) == 0)
        return SURDUR;
    else if (strcmp(commands[5], input) == 0)
        return OLDUR;
    else if (strcmp(commands[6], input) == 0)
        return KAPAT;
    // mevcut komut listesinde bulunmayan bir komut girilmisse, bu komut ya hatalidir.
    else{
        printf("Hatali bir komut girdiniz. Mevcut komutlar: ");
        int i;
        for(i = 0; i<7; i++) printf("%s | ", commands[i]);
        printf("\n");
        return HATA;
    }
}


int main() {
    char *term = "yenishell> ";
    char *commands[20]; //input parse edilerek bu degiskende tutulur
    int check = 1;

    while (check) {
        pid_t pid;
        int status;

        char input[2048];
        printf("%s", term);
        fgets(input, 2048, stdin);


        // input, ilk kelimesi alinmak uzere parse ediliyor.
        // commands[0] da baslat, beklet vb. komutlar tutuluyor.
        commands[0] = strtok(input, " \t\n");
        if (commands[0] == NULL)
            continue;

        // komutun devamindaki kelimeler parse edilerek commands
        // dizisine ekleniyor.
        int numWords = 1;
        for (; numWords < 20; ++numWords) {
            commands[numWords] = strtok(0, " \t\n");
            // parse edilecek baska kelime kalmadiginda strtok fonksiyonu
            // NULL dondurur. Bu durumda parse islemi bitirilmeli.
            if (commands[numWords] == NULL) break;
        }

        commands[numWords] = NULL;


        // girilen komuta gore (baslat, surdur vb.) case'ler calisacak.
        switch(check_command(commands[0])){

            case BASLAT:
                // baslat komutu yanina bir de parametre almak zorunda.
                // bu nedenle kelimeden az olursa hata verilecek
                if (numWords < 2) {
                    printf("%sYanlis sayida arguman girildi. Kullanim: başlat <program> [<arg1> <arg2> ...]\n", term);
                    continue;
                }

                pid = fork();

                // fork cagrisinin dondugu deger negatif ise hata olusmustur
                if (pid < 0) {
                    printf("%sfork: %s.\n", term, strerror(errno));
                    continue;
                }
                else if (pid == 0) {
                    // child process de komut calistirilir
                    if (execvp(commands[1], commands + 1) < 0) {
                        printf("%sexecvp: %s.\n", term, strerror(errno));
                        continue;
                    }
                }
                // parent process
                else {
                    printf("%sProcess %d baslatildi.\n", term, pid);
                }

                usleep(100000); //bazi durumlarda yenishell satiri cikmiyor. bu sorunu cozmek amacli bir ekleme.
                break;


            /*--------------------------------------------*/
            case BEKLET:
                // beklet komutu tek bir parametre almakta. Parametre sayisi
                // bundan fazla ise hata verilir.
                if (numWords > 1) {
                    printf("%sYanlis sayida arguman girildi. Kullanim: beklet \n", term);
                    continue;
                }

                pid = wait(&status);

                if (pid == -1) {
                    // Process kalmadi ise
                    if (errno == ECHILD)
                        printf("%sGeride process kalmadi.\n", term);
                    // baska bir hata mevcut
                    else
                        printf("%sbeklet: %s\n", term, strerror(errno));
                }
                // wait() basarili
                else if (status == 0)
                    printf("%sProcess %d exited normally with status %d.\n", term, pid, status);
                // wait() hata olustu
                else
                    printf("%sProcess %d exited abnormallly with status %d: %s.\n", term, pid, status,
                           strsignal(status));

                break;


            /*--------------------------------------------*/
            case YURUT:

                pid = fork();

                if (pid == 0){
                    if (execvp(commands[1], commands + 1) < 0) {
                        printf("%sexecvp: %s.\n", term, strerror(errno));
                    }
                }
                else if (pid > 0){
                    pid_t ret = waitpid(pid, &status, 0);
                    if(ret == -1) {     //hata olusmus ise
                        printf("%syurut hata: %s\n", term, strerror(errno));
                    }
                    if(status == 0) {   //sorunsuz calismis
                        printf("%sProcess %d exited normally with status %d.\n", term, pid, status);
                    }
                    else{
                        printf("%sProcess %d exited abnormally with status %d: %s.\n", term, pid, status, strsignal(status));
                    }
                }
                else {
                    printf("%sfork: %s.\n", term, strerror(errno));
                }

                break;


            /*--------------------------------------------*/
            case DURDUR:
                // arguman sayisi kontrolu yapiliyor
                if (numWords != 2) {
                    printf("%sYanlis sayida arguman girildi. Kullanim: durdur <pid>\n", term);
                    continue;
                }

                pid = atoi(commands[1]);
                // Verilen pid degerinin integer olup olmadigi kontrol ediliyor.
                // ornegin 'durdur deneme' gibi bir input girilirse, atoi fonksiyonu
                // 0 degerini donecektir. Bu da hatali bir durumdur.
                if (pid == 0){
                    printf("%sHatali bir pid degeri. Kullanim:  durdur <pid>\n", term);
                }
                status = kill(pid, SIGSTOP);

                if(status == 0)
                    printf("%sprocess %d durduruldu\n", term, atoi(commands[1]));
                else if(status < 0)
                    printf("%sprocess durdurulamadi: %s\n", term, strerror(errno));

                break;

            /*--------------------------------------------*/
            case SURDUR:
                if (numWords != 2) {
                    printf("%sYanlis sayida arguman girildi. Kullanim: sürdür <pid>\n", term);
                    continue;
                }

                pid = atoi(commands[1]);
                // Verilen pid degerinin integer olup olmadigi kontrol ediliyor
                if (pid == 0){
                    printf("%sHatali bir pid degeri. Kullanim: sürdür <pid>\n", term);
                }
                status = kill(pid, SIGCONT);

                if(status == 0)
                    printf("%sprocess %d surduruldu\n", term, atoi(commands[1]));
                else if(status < 0)
                    printf("%sprocess surdurulemedi: %s\n", term, strerror(errno));

                break;

            /*--------------------------------------------*/
            case OLDUR:
                if (numWords != 2) {
                    printf("%sYanlis sayida arguman girildi. Kullanim: öldür <pid>\n", term);
                    continue;
                }

                pid = atoi(commands[1]);
                // Verilen pid degerinin integer olup olmadigi kontrol ediliyor
                if (pid == 0){
                    printf("%sHatali bir pid degeri. Kullanim: öldür <pid>\n", term);
                }
                status = kill(pid, SIGKILL);

                if(status == 0)     //process sorunsuz bir sekilde olduruldu
                    printf("%sprocess %d olduruldu\n", term, atoi(commands[1]));
                else if(status < 0) // bir hata olustu
                    printf("%sprocess oldurulemedi: %s\n", term, strerror(errno));

                break;


            /*--------------------------------------------*/
            case KAPAT:
                exit(0);

            // bosluk veya hatali bir komut girildi
            default:
                break;



        }


    }

    return 0;
}




























