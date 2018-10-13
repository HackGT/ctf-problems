# Flag Description

This flag is a simple SaaS notepad application that protects its cookies with a custom hash.
Competitors must reverse-engineer the hash to modify the data serialized in the cookie to set the `found_flag` value to `true`.
The hash is implemented as follows:

Interpret the input as a sequence of 64-bit big-endian integers,
padding on the right with zeros as necessary to make the length a multiple of 64 bits.
Calculate the sum of all of these integers mod 9,223,372,036,854,775,783 (`0x7fff_ffff_ffff_ffe7`)
which is the largest prime number smaller than 2^63.

# Expected Solution

Contestants should examine the cookie value.
It is two base64-encoded strings separated by a period.
The first part is a JSON document containing the keys `found_flag` and `notes`.
The `notes` key contains whatever is typed in the field.
The `found_flag` key is `false`.
The second part initially appears random;
I will call it the "check".

I poked at the server with this Python function in a REPL,
but any equivalent action will do:

```python
from base64 import b64decode
from urllib.parse import unquote

from requests import post


def ex(v):
    cook = post('http://localhost:8000/', data={'notes': v}).cookies['state']
    data, dot, check = cook.partition('.')
    return b64decode(unquote(data)), unquote(check)
```

The first thing you should note is that the check is deterministic.
You have partial control over the plaintext,
so start attacking the hash.

The next thing to note is that the output is always 12 chars with one pad.
That means that the decoded form is always (12 * 3/4 - 1) = 8 bytes.

This is the part I'm worried about:
you need a hunch that the input is being handled in 8-byte chunks.

```python
from itertools import islice


def chunks(it):
    it = iter(it)
    while True:
        r = bytes(islice(it, 8))
        if not r:
            break
        yield r


def ex(v):
    cook = post('http://localhost:8000/', data={'notes': v}).cookies['state']
    data, dot, check = cook.partition('.')
    for ck in chunks(b64decode(unquote(data))):
        print(ck)
    print(list(b64decode(unquote(check))))
```


This allows us to see what the effect of a single chunk of input is on the output.

```pycon
>>> ex('---        ')
b'{"found_'
b'flag":fa'
b'lse,"not'
b'es":"---'
b'        '
b'"}'
[83, 149, 111, 92, 252, 100, 170, 73]
>>> ex('---       !')
b'{"found_'
b'flag":fa'
b'lse,"not'
b'es":"---'
b'       !'
b'"}'
[83, 149, 111, 92, 252, 100, 170, 74]
>>> ex('---      ! ')
b'{"found_'
b'flag":fa'
b'lse,"not'
b'es":"---'
b'      ! '
b'"}'
[83, 149, 111, 92, 252, 100, 171, 73]
```

It looks like each block is just added, perhaps with a magic start number.
Let's see:

```python
from itertools import zip_longest

# From itertools docs:
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def ex(v):
    cook = post('http://localhost:8000/', data={'notes': v}).cookies['state']
    data, dot, check = cook.partition('.')
    thesum = sum(int.from_bytes(bytes(ck), 'big') for ck in grouper(b64decode(unquote(data)), 8, 0))
    print((thesum & 0xFFFF_FFFF_FFFF_FFFF) - int.from_bytes(b64decode(unquote(check)), 'big'))
```

```pycon
>>> ex('---        ')
9223372036854775733
>>> ex('---       !')
9223372036854775733
>>> ex('---      ! ')
9223372036854775733
>>> ex('---!       ')  # '!' == ' ' + 0x01
9223372036854775733
>>> ex('---#       ')  # '#' == ' ' + 0x03 (' ' + 0x02 is '"', but JSON)
9223372036854775733
>>> ex('---$       ')  # '$' == ' ' + 0x04
9223372036854775733
>>> ex('---(       ')  # '(' == ' ' + 0x08
9223372036854775733
>>> ex('---0       ')  # '0' == ' ' + 0x10
-100
```

Interesting.
It's not just the sum wrapping around
(and we could have guessed that because it would be too easy).

The smallest printable ASCII is 0x20 ` `.
The largest is 0x7e `~`.
We'll start with a block full of spaces and find where adding a power of two makes it wrap.

```python
def ex(v):
    cook = post('http://localhost:8000/', data={'notes': v}).cookies['state']
    data, dot, check = cook.partition('.')
    return '{:16x}'.format(int.from_bytes(b64decode(unquote(check)), 'big'))
```


```pycon
>>> ex('---        ')
'76126f5cfc6487cc'
>>> ex('---!       ') # ! is 0x21
'77126f5cfc6487cc'
>>> ex('---$       ') # $ is 0x24 (0x22 is ", but that's special in JSON)
'7a126f5cfc6487cc'
>>> ex('---(       ') # ( is 0x28
'7e126f5cfc6487cc'
>>> ex('---0       ') # 0 is 0x30
' 6126f5cfc6487e5'
>>> hex(0x7e126f5cfc6487cc + 0x0800_0000_0000_0000 - 0x6126f5cfc6487e5)
'0x7fffffffffffffe7'
```

Now we've found our modulus:

```python
import re
from base64 import b64encode
from json import dumps
from urllib.parse import quote

from requests import get

MODULUS = 0x7fffffffffffffe7

def checksum(s):
    thesum = sum(int.from_bytes(bytes(ck), 'big') for ck in grouper(s, 8, 0))
    return (thesum % MODULUS).to_bytes(8, 'big')
```

```pycon
>>> payload = dumps({'found_flag': True, 'notes': ''}).encode('ascii')
>>> cookie = '{}.{}'.format(quote(b64encode(payload)), quote(b64encode(checksum(payload))))
>>> resp = get('http://localhost:8000/', cookies={'state': cookie})
>>> re.search(r'hackgt\{.*?\}', resp.text).group(0)
'hackgt{9FRDzk4T51gKTifO}'
```
