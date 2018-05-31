f = open('florida.pdf', 'rb')

x = f.read()

spin_bby = 620

y = x[spin_bby:]
z = x[:spin_bby]

new = y + z
f.close()

f = open('flo.rida', 'wb')
f.write(new)
f.close()
