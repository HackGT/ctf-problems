import base64
import sys
from Crypto.Cipher import AES
from Crypto import Random

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

enc = base64.b64decode("vLhwqOzqjA4s1Mjh/WKa18OR9snTmIcroJ+Fg+ipa4yqsd5oc7+TG0jqdOtd43M6u26UqjAnMqfoTM0TsdpqwQ==")
re_enc = base64.b64encode(enc[:16] + bytes(0) * 16 + enc[16:])
print re_enc