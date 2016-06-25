// Batuhan Buyukguzel
// 111101035


#include <stdio.h>      //printf(), perror(), sprintf()
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>     //read(), write() and close()
#include <fcntl.h>      //open()
#include <sys/stat.h>   //mkdir()
#include <libgen.h>     //basename(), direname()
#include <errno.h>
#include <memory.h>


#define BUFFER_SIZE 4096


// Parse edilen directory, append edilerek bu global degiskende saklanir.
char newPath[255];


// Kopyalama islemi 2 saniyeden uzun surerse, bu fonksiyon
// yardimiyla ekrana birer saniye araliklarla islemin
// devam ettigi bilgisi yazdirilir.
void display_message() {
    printf("Kopyalama islemi devam ediyor...\r");
    fflush(stdout);
    alarm(1);
}


// Kodun calismasi sirasinda hedef konum bilgisi delimiter olarak "/"
// karakteri kullanilarak parse edilir. Daha sonra verilen konumdaki
// her directory ismi bu fonksiyon yardimiyla newPath degiskenine append edilir.
void concatWithCurrDir(char *dir) {
    strcat(newPath, "/");
    strcat(newPath, dir);
}


// Parametre olarak verilen bir konumun klasör olup olmadiginin kontrolu
// yapilir. Eger verilen directory mevcut ise 1, degilse 0 donulur.
int isDirExists(struct stat st, char *directory) {
    if (!stat(directory, &st)) {
        if (S_ISDIR(st.st_mode))
            return 1;
        return 0;
    }
    return 0; //gerekli mi?
}


// Parametre olarak verilen path yapisinda dolasarak olmayan directory'leri olusturur
// ve bir alt dizine inerek ayni isleme devam eder.
void checkFolderStructure(char *directory, int *nDir_fd){
    char *dir;
    struct stat st;
    char *segFaultCheck = ".";

    // Verilen directory (path), "/" karakterine gore split edilir ve path'deki ilk
    // directory elde edilir.
    if (strcmp(directory, segFaultCheck) != 0){
        dir = strtok(directory, "/");
        // dir, newPath degiskenine append edilir.
        concatWithCurrDir(dir);
        chdir(newPath);
        while (dir != NULL) {
            if (chdir(newPath) == 0) {
                ; // bir sey yapma
            }
            else {
                if (isDirExists(st, newPath)) {
                    printf("Error when checking directory: %s\n", newPath);
                    perror("Error");
                    exit(1);
                }
                else {
                    *nDir_fd = mkdir(newPath, 0777);
                    // klasor olusturulurken bir hata meydana gelmisse
                    if (*nDir_fd == -1) {
                        // olusan hata, "klasor mevcut" hatasindan baska bir hata ise
                        // programdan cik.
                        if (errno != EEXIST) {
                            printf("Error when creating directory %s\n", newPath);
                            perror("Error");
                            exit(1);
                        }
                        // klasor mevcut hatasi ise birsey yapmaya gerek yok
                    }
                    // klasor basariyla olusturuldu
                }
            }
            // bir sonraki klasor adini parse et
            dir = strtok(NULL, "/");
            // parse isleminde sona gelinmemisse isleme devam et
            if (dir != NULL)
                concatWithCurrDir(dir);
            else // sona gelinmisse donguyu sonlandir
                break;
        }
    }

}


int copyFile(char *source_file, char *new_file){
    int sFile_fd, nDir_fd, nFile_fd;
    char buffer[BUFFER_SIZE];
    int num_read;
    long totalSize = 0;


    // Hedef konum bilgisi parse edilerek dosya adi bilgisi alinir.
    char *filename = basename(new_file);
    // Hedef konum bilgisi parse edilerek path bilgisi alinir.
    char *directory = dirname(new_file);


    // Kaynak dosya acilir. Dosyanin acilmasi sirasinda bir hata olusursa
    // ilgili hata bilgisi ekrana yazdirilir.
    sFile_fd = open(source_file, O_RDONLY, 0);
    if (sFile_fd == -1) {
        perror("Error opening source file");
        exit(1);
    }


    // Kopyalama isleminin, verilen klasor yapisina uygun hale getirilmesi
    // icin bu fonksiyon cagrilarak eksik klasorler olusturulur.
    checkFolderStructure(directory, &nDir_fd);


    // Arguman olarak verilmis olan newPath degiskenin icerigi basename/dirname
    // fonksiyonlari tarafindan degistirildigi icin burada kucuk bir concat
    // islemi yapilir.
    sprintf(new_file, "%s/%s", newPath, filename);

    // Yeni dosya, ilgili dosya adiyla, yazilmak uzere acilir/olusturulur.
    // Dosyanin acilmasi sirasinda bir hata olusursa
    // ilgili hata bilgisi ekrana yazdirilir.
    nFile_fd = open(new_file, O_WRONLY | O_EXCL | O_CREAT, 0644);
    if (nFile_fd == -1) {
        perror("Error opening new file");
        if (errno == EISDIR)
            printf("Hedef dosyayi [/dosya] seklinde, basinda / isaretiyle girmeniz geriyor olabilir.\n");
        exit(1);
    }


    // Kaynak dosyadan, buffer boyutu kadar byte okunur. Eger okuma
    // sonucunda 0 dan farkli sayida byte okunmus ise islem basarilidir,
    // donguye tekrar girilir. Okunan bytelar, yeni dosyaya yazilir ve
    // yazilan toplam byte sayisinin tutuldugu totalSize degiskeninin
    // icerigi guncellenir.
    while ((num_read = read(sFile_fd, &buffer, BUFFER_SIZE)) > 0) {
        write(nFile_fd, &buffer, num_read);
        totalSize = totalSize + num_read;
    }


    // Kopyalanan toplam byte bilgisi ekrana yazdirilir.
    printf("\nToplam %ld byte kopyalandi.\n\n", totalSize);


    // Tum file handler'lar kapatilir.
    // Source file descriptor, New directory file descriptor ve New file file descriptor
    close(sFile_fd);
    close(nDir_fd);
    close(nFile_fd);
}



int main(int argc, char *argv[]) {
    char *source_file;
    char *new_file;

    // Program calistirilirken verilen argumanların dogru sekilde
    // olup olmadigi kontrolu yapilmaktadir. Eger argumanlar dogru
    // sekilde verildiyse, kaynak dosya ve yeni dosya bilgisi ilgili
    // degiskenlere atanir.
    if (argc == 3) {
        source_file = argv[1];
        new_file = argv[2];
    }

    // Argumanlar hatali bir sekilde verilmisse ekrana dogru sekli yazdirilir.
    else {
        printf("Programi yanlis sekilde calistirdiniz.\n");
        printf("Dogrusu su sekilde olmalidir: ./kopyala /dirx/../kaynak_dosya /diry/../yeni_dosya\n");
        exit(1);
    }


    // Kopyalama isleminin 2 saniyeden uzun surmesi durumunda ekranda bilgi
    // mesaji gosterilmesi icin bir signal olusturulur ve alarm 2 saniyeye
    // ayarlanir.
    signal(SIGALRM, display_message);
    alarm(2);


    // Kopyalama islemi baslatilir.
    copyFile(source_file, new_file);


    alarm(0);
    return 0;
}