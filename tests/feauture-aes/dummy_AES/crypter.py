# OMG https://stackoverflow.com/questions/11567290/cryptojs-and-pycrypto-working-together

import base64
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
key = b"1234567890123456" # TODO change to something with more entropy

def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + chr(length)*length

def unpad(data):
    # return data[:-ord(data[-1])]
    return data
   # return data[:data[-1]]


def encrypt(message, key):
    IV = Random.new().read(BLOCK_SIZE)
    aes = AES.new(key, AES.MODE_CBC, IV)
    return base64.b64encode(IV + aes.encrypt(pad(message)))

def decrypt(encrypted, key):
    encrypted = base64.b64decode(encrypted)
    IV = encrypted[:BLOCK_SIZE]
    aes = AES.new(key, AES.MODE_CBC, IV)
#     return unpad(aes.decrypt(encrypted[BLOCK_SIZE:]))
    return aes.decrypt(encrypted[BLOCK_SIZE:])
