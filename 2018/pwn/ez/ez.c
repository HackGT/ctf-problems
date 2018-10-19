#include <unistd.h>
#include <stdio.h>
#include <stdint.h>
int main(){char a[300];printf("%lu\n",(uintptr_t)a);fflush(stdout);read(0,a,500);}