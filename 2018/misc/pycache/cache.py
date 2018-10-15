MEM_SIZE = 256
CACHE_SIZE = 32

import functools
import re
import sys
import time

REGEX_CC = 'clear'
REGEX_LD = '^ld (?P<dst_reg>[a-d]) (?P<addr>[0-9]*)$'
REGEX_LDI = '^ldi (?P<dst_reg>[a-d]) (?P<addr_reg>[a-d])$'
REGEX_ST = '^st (?P<value_reg>[a-d]) (?P<addr>[0-9]*)$'
REGEX_STI = '^sti (?P<value_reg>[a-d]) (?P<addr_reg>[a-d])$'
REGEX_MV_LIT = '^mvl (?P<dst_reg>[a-d]) (?P<value>[0-9]*)$'
REGEX_MV_REG = '^mvr (?P<dst_reg>[a-d]) (?P<src_reg>[a-d])$'


def timeme(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        return time.time() - start_time
    return inner


class Processor:
    def __init__(self, initial_path):
        self.memory = Memory()
        self.regs = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': 0
        }

        with open(initial_path, 'rb') as fh:
            contents = fh.read()
        if len(contents) > MEM_SIZE:
            raise ValueError
        for index, byte in enumerate(contents):
            self.memory.write(index, ord(byte))
        self.clear_cache()

    @timeme
    def clear_cache(self):
        self.memory.clear_cache()

    @timeme
    def ld_direct(self, dst_reg, addr):
        if dst_reg not in self.regs.keys():
            raise ValueError
        self.regs[dst_reg] = self.memory.read(addr)

    @timeme
    def ld_indirect(self, dst_reg, addr_reg):
        if dst_reg not in self.regs.keys() or addr_reg not in self.regs.keys():
            raise ValueError
        self.regs[dst_reg] = self.memory.read(self.regs[addr_reg])

    @timeme
    def st_direct(self, value_reg, addr):
        if value_reg not in self.regs.keys():
            raise ValueError
        self.memory.write(addr, self.regs[value_reg])

    @timeme
    def st_indirect(self, value_reg, addr_reg):
        if (value_reg not in self.regs.keys() or
                addr_reg not in self.regs.keys()):
            raise ValueError
        self.memory.write(self.regs[addr_reg], self.regs[value_reg])

    @timeme
    def move_literal(self, dst_reg, value):
        if dst_reg not in self.regs.keys():
            raise ValueError
        if value < 0 or value > 255:
            raise ValueError
        self.regs[dst_reg] = value

    @timeme
    def move_reg(self, dst_reg, src_reg):
        if not dst_reg in self.regs.keys() or not src_reg in self.regs.keys():
            raise ValueError
        self.regs[dst_reg] = self.regs[src_reg]


class Memory:
    def __init__(self):
        self.mem = [0] * MEM_SIZE
        self.cache = Cache()

    def read(self, addr):
        if addr < 0 or addr > (MEM_SIZE - 1):
            raise ValueError
        try:
            return self.cache.read(addr)
        except ValueError:
            time.sleep(.1)
            value = self.mem[addr]
            self.cache.write(addr, value)
            return self.mem[addr]

    def write(self, addr, value):
        if addr < 0 or addr > (MEM_SIZE - 1):
            raise ValueError
        if value < 0 or value > 255:
            raise ValueError
        self.cache.write(addr, value)
        self.mem[addr] = value

    def clear_cache(self):
        self.cache.clear()


class CacheEntry:
    def __init__(self, value):
        self.value = value
        self.ts = time.time()

    def touch(self):
        self.ts = time.time()


class Cache:
    def __init__(self):
        self.cache = {}

    def read(self, addr):
        if addr < 0 or addr > (MEM_SIZE - 1):
            raise ValueError
        if addr not in self.cache:
            raise ValueError

        entry = self.cache[addr]
        entry.touch()
        return entry.value

    def write(self, addr, value):
        if addr < 0 or addr > (MEM_SIZE - 1):
            raise ValueError
        if value < 0 or value > 255:
            raise ValueError
        if addr in self.cache:
            self.cache[addr] = CacheEntry(value)
            return

        if len(self.cache) >= CACHE_SIZE:
            self._evict()
        self.cache[addr] = CacheEntry(value)

    def _evict(self):
        eviction_addr = None
        for addr in self.cache.keys():
            if eviction_addr is None:
                eviction_addr = addr
            elif self.cache[eviction_addr].ts > self.cache[addr].ts:
                eviction_addr = addr
        del self.cache[eviction_addr]

    def clear(self):
        self.cache = {}


def main():
    p = Processor('/pycache/flag.txt')
    while True:
        try:
            sys.stdout.flush()
            line = sys.stdin.readline().strip()
            m = re.match(REGEX_CC, line)
            if m:
                print(p.clear_cache())
                continue
            m = re.match(REGEX_LD, line)
            if m:
                print(p.ld_direct(m.group('dst_reg'), int(m.group('addr'))))
                continue
            m = re.match(REGEX_LDI, line)
            if m:
                print(p.ld_indirect(m.group('dst_reg'), m.group('addr_reg')))
                continue
            m = re.match(REGEX_ST, line)
            if m:
                print(p.st_direct(m.group('value_reg'), int(m.group('addr'))))
                continue
            m = re.match(REGEX_STI, line)
            if m:
                print(p.st_indirect(m.group('value_reg'), m.group('addr_reg')))
                continue
            m = re.match(REGEX_MV_LIT, line)
            if m:
                print(p.move_literal(m.group('dst_reg'), int(m.group('value'))))
                continue
            m = re.match(REGEX_MV_REG, line)
            if m:
                print(p.move_reg(m.group('dst_reg'), m.group('src_reg')))
                continue
            raise ValueError
        except ValueError:
            print('Invalid command')
            return

if __name__ == '__main__':
    try:
        main()
    except Exception:
        pass
