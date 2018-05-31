from Crypto.Cipher import AES

obj = AES.new('hackgt{oracle_arena_sux_go_cavs}', AES.MODE_CBC, '0000000000000000')
message = "hello world"
padding = 16 - len(message)
print len(
ciphertext = obj.encrypt(message + '/x00' * 16)

print ciphertext
