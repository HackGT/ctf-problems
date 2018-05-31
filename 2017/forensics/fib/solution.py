f = open('flo.rida', 'rb')
x = f.read()
spin_bby = 620
y = x[len(x) - spin_bby:]
z = x[:len(x) - spin_bby]

new = y + z
f.close()

f = open('flo.rida.out', 'wb')
f.write(new)
f.close()
