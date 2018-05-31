import random
import base64

from caesarcipher import CaesarCipher

flag = "hackgt{how_does_encoding_work}"

current = flag
for i in range(15):
    if bool(random.randint(0,1)):
        print 'encode'
        current = base64.b64encode(current)
    else:
        print 'shift'
        current = CaesarCipher(current, 13).encoded
print current
num = 0
print ''
print 'start'
while num < 15:
    try:
        print 'decode'
        current = base64.b64decode(current)
        num += 1
    except:
        print 'shift'
        break