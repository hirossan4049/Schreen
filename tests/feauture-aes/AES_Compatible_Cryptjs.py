import os, json
import binascii
from Crypto import Random
from Crypto.Cipher import AES
 
# ------------------------------
# DEFINE Encryption Class
class Cryptor(object):
    # AES-256 key (32 bytes)
    KEY = "01ab38d5e05c92aa098921d9d4626107133c7e2ab0e4849558921ebcc242bcb0"
    BLOCK_SIZE = 16
    
    @classmethod
    def _pad_string(cls, in_string):
        '''Pad an input string according to PKCS#7'''
        in_len = len(in_string)
        pad_size = cls.BLOCK_SIZE - (in_len % cls.BLOCK_SIZE)
        return in_string.ljust(in_len + pad_size, chr(pad_size))
    
    @classmethod
    def _unpad_string(cls, in_string):
        '''Remove the PKCS#7 padding from a text string'''
        in_len = len(in_string)
        print(in_string[-1])
        pad_size = ord(str(in_string[-1]))
        print(pad_size,cls.BLOCK_SIZE)
        print(in_string[:in_len - pad_size])
        if pad_size > cls.BLOCK_SIZE:
            raise ValueError('Input is not padded or padding is corrupt')
        return in_string[:in_len - pad_size]
    
    @classmethod
    def generate_iv(cls, size=16):
        return Random.get_random_bytes(size)
    
    @classmethod
    def encrypt(cls, in_string, in_key, in_iv=None):
        key = binascii.a2b_hex(in_key)
        
        if in_iv is None:
            iv = cls.generate_iv()
            in_iv = binascii.b2a_hex(iv)
        else:
            iv = binascii.a2b_hex(in_iv)
        
        aes = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
        return in_iv, aes.encrypt(cls._pad_string(in_string))
    
    @classmethod
    def decrypt(cls, in_encrypted, in_key, in_iv):
        key = binascii.a2b_hex(in_key)
        iv = binascii.a2b_hex(in_iv)
        aes = AES.new(key, AES.MODE_CFB, iv, segment_size=128)      
        
        decrypted = aes.decrypt(binascii.a2b_base64(in_encrypted).rstrip())
        return cls._unpad_string(decrypted)
