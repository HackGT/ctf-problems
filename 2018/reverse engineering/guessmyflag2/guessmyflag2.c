#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char ans[17] = {103, 14, 111, 0, 97, 28, 105, 26, 122, 20, 102, 13, 107, 23, 98, 31};

int main(int argc, const char* argv[]) {
    FILE *f;
    f = fopen("./flag.txt", "r");
    if (f == NULL) {
        printf("Something wrong, please contact the admins\n");
        exit(0);
    }
    char flag[64];
    int ind = 0;
    char c;
    while ((c = getc(f)) != EOF) {
        flag[ind++] = c;
    }
    flag[ind] = '\0';
    char input[17];
    printf("Would you like my flag?\n");
    fgets(input, 17, stdin);
    input[16] = '\0';
    for (int i = 0; i < 17; i++) {
        if (i % 2 == 0) {
            input[i] ^= i;
        } else {
            input[i] ^= input[i - 1];
        }
    }
    if (!memcmp(input, ans, 16)) {
        puts(flag);
    } else {
        printf("You guessed wrong!\n");
    }
    return 0;
}