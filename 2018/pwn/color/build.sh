gcc -fno-stack-protector -fno-pie -no-pie -o color color.c
python change_exec.py color
strip color
