#include <stdio.h>
#include <bsd/stdlib.h>

struct chainState {
    int prob[10];
};

struct chainState amc[] = {
    {0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0},
    {1,4,0,0,1,0,1,0,1,0},
    {3,0,2,0,0,0,0,0,1,1},
    {4,1,1,0,0,0,0,2,0,1},
    {7,4,0,0,2,0,3,1,0,0},
    {1,2,2,0,1,0,0,3,2,0},
    {3,2,1,0,0,0,1,0,7,0},
    {1,3,0,0,0,7,0,1,0,4},
    {2,7,0,0,1,0,2,0,1,0},
};

int jumpRandom(int currState) {
    int total = 0;
    for (int i = 0; i < 10; i++) {
        total += amc[currState].prob[i];
    }
    int choice = arc4random_uniform(total);
    int ptr = 0;
    while (1) {
        choice -= amc[currState].prob[ptr];
        if (choice < 0) {
            return ptr;
        }
        ptr++;
    }
}

int main() {
    unsigned char byte;
    for (int i = 0; i < 8; i++) {
        int state = i + 2;
        while (state > 1) {
            state = jumpRandom(state);
        }
        byte |= (state << i);
    }
    printf("%02x\n", byte);
}
