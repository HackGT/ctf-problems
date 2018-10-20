#include <stdio.h>
#include <stdlib.h>

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
    char input[64];
    printf("Guess my number:\n");
    fgets(input, 64, stdin);
    if (atoi(input) == 27384639) {
        puts(flag);
    } else {
        printf("You guessed wrong!\n");
    }
    return 0;
}