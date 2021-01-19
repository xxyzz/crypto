#!/usr/bin/env python3

'''
In this project you will implement two encryption/decryption systems, one using
AES in CBC mode and another using AES in counter mode(CTR). In both cases the
16-byte encryption IV is chosen at random and is prepended to the ciphertext.

For CBC encryption we use the PKCS5 padding scheme discussed in the lecture
(14:04). While we ask that you implement both encryption and decryption, we
will only test the decryption function. In the following questions you are
given an AES key and a ciphertext(both are hex encoded) and your goal is
to recover the plaintext and enter it in the input boxes provided below.

For an implementation of AES you may use an existing crypto library such as
PyCrypto(Python), Crypto++(C++), or any other. While it is fine to use the
built-in AES functions, we ask that as a learning experience you implement
CBC and CTR modes yourself.
'''

import os

# dinosaurs with laser guns!
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AES():
    def __init__(self, key, mode):
        self.key = bytes.fromhex(key)
        self.mode = mode
        self.cipher = Cipher(algorithms.AES(self.key), modes.ECB())

    def decrypt(self, ct):
        iv = bytes.fromhex(ct)[:16]
        ct_bytes = bytes.fromhex(ct)[16:]
        pt = ''
        if self.mode == 'CBC':
            '''
            IV  c0      c1
            |   |----|  |
            |  D(k,) | D(k,)
            |   |    |  |
             -> ⊕    -> ⊕
                m0      m1
            '''
            decryptor = self.cipher.decryptor()
            previous_ct = iv
            for i in range(0, len(ct_bytes), 16):
                ct_block = ct_bytes[i:i+16]
                pt_block = [a ^ b for (a, b) in zip(
                    previous_ct, decryptor.update(ct_block))]
                if i == len(ct_bytes) - 16:  # rm padding
                    pt_block = pt_block[:-pt_block[-1]]
                previous_ct = ct_block
                pt += ''.join([chr(c) for c in pt_block])
        elif self.mode == 'CTR':
            '''
            IV  c0       c1
                ⊕        ⊕
                E(k,IV)   E(k,IV+1)
                m0       m1
            '''
            encryptor = self.cipher.encryptor()
            iv = int.from_bytes(iv, byteorder='big')
            for i in range(0, len(ct_bytes), 16):
                ct_block = ct_bytes[i:i+16]
                data = (iv+i//16).to_bytes(16, byteorder='big')
                pt_block_bytes = [a ^ b for (a, b) in zip(
                    ct_block, encryptor.update(data)[:len(ct_block)])]
                pt += ''.join([chr(c) for c in pt_block_bytes])
        return pt

    def encrypt(self, pt, iv):
        pt_bytes = pt.encode('utf-8')
        encryptor = self.cipher.encryptor()
        ct = iv
        if self.mode == 'CBC':
            '''
            IV  m0      m1
            |   |       |
            --> ⊕   |-> ⊕
                |   |   |
              E(k,) |  E(k,)
                |---    V
            IV  c0      c1
            '''
            previous_ct = bytes.fromhex(iv)
            if len(pt_bytes) % 16 == 0:
                pt_bytes += bytes([16]) * 16  # dummy pad
            for i in range(0, len(pt_bytes), 16):
                pt_block = pt_bytes[i:i+16]
                pad = 16 - len(pt_block)
                pt_block += bytes([pad]) * pad
                previous_ct = encryptor.update(bytes([a ^ b for (a, b) in zip(
                    previous_ct, pt_block)]))
                ct += previous_ct.hex()
        elif self.mode == 'CTR':
            iv = int(iv, 16)
            for i in range(0, len(pt_bytes), 16):
                pt_block = pt_bytes[i:i+16]
                data = (iv+i//16).to_bytes(16, byteorder='big')
                ct_block = [a ^ b for (a, b) in zip(
                    pt_block, encryptor.update(data)[:len(pt_block)])]
                ct += bytes(ct_block).hex()
        return ct


CBC_key = '140b41b22a29beb4061bda66b6747e14'
CBC_cts = ('4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2'
           'e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81',
           '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e'
           '713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253')
aes = AES(CBC_key, 'CBC')
for ct in CBC_cts:
    print(aes.decrypt(ct))

CTR_key = '36f18357be4dbd77f050515c73fcf9f2'
CTR_cts = ('69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc38'
           '8d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f'
           '51eeca32eabedd9afa9329',
           '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0'
           'e311bde9d4e01726d3184c34451')
aes = AES(CTR_key, 'CTR')
for ct in CTR_cts:
    print(aes.decrypt(ct))


key = os.urandom(16).hex()
iv = os.urandom(16).hex()
message = 'Believe... I know it sounds like a cat poster but it\'s true.'
aes = AES(key, 'CTR')
assert(aes.decrypt(aes.encrypt(message, iv)) == message)
aes = AES(key, 'CBC')
assert(aes.decrypt(aes.encrypt(message, iv)) == message)
message = '1234567890123456'
assert(aes.decrypt(aes.encrypt(message, iv)) == message)
