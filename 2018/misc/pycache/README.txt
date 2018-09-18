PyCache is a cache simulator written in Python! It can be used to measure the latency of different access patterns.

PyCache's memory unit has 256 bytes of memory. The memory is byte-addressable. It has a 32-wide fully associative cache. It has four registers (a, b, c, and d) that can be used to hold byte values.

Instructions:

clear - Clear the cache
    clear

ld $dst_reg $addr - Load from address specified in $addr into the reg $dst_reg.
    ld a, 10 - read the byte at address 10 into register a

ldi $dst_reg $addr_reg - Load the value from the address specified in $addr_reg into $dst_reg.
    ldi b, c - If register c is 55, read the byte at address 55 into register a

st $value_reg, $addr - Store the value from register $value_reg into address $addr.
    st a, 10 - store the byte in register a into address 10

sti $value_reg, $addr_reg - Store the value in register $value_reg into the address specified by $addr_reg.
    sti c, d - If register d is 27, store the value in register c into address 27

mvl $dst_reg, $value - Move the literal $value into register $dst_reg.
    mvl a, 190 - Set register a to 190

mvr $dst_reg, $src_reg - Move the value in $src_reg into register $dst_reg.
    mvr a, b - If register b is 255, set register a to 255.


Each time you issue a command, PyCacheSim will reply with the amount of time it took to execute the command.
