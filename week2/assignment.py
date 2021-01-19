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

# dinosaurs with laser guns!
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AES():
    def __init__(self, key, mode):
        self.key = bytes.fromhex(key)
        self.mode = mode
        self.cipher = Cipher(algorithms.AES(self.key), modes.ECB())

    def encrypt(self, pt, iv):
        if self.mode == 'CBC':
            pass

    def decrypt(self, ct):
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
            iv = bytes.fromhex(ct)[:16]
            for i in range(0, len(ct_bytes), 16):
                ct_block = ct_bytes[i:i+16]
                if i == 0:
                    pt_block_bytes = [a ^ b for (a, b) in zip(
                        iv, decryptor.update(ct_block))]
                    pt += ''.join([chr(c) for c in pt_block_bytes])
                else:
                    previous_ct = ct_bytes[i-16:i]
                    pt_block_bytes = [a ^ b for (a, b) in zip(
                        previous_ct, decryptor.update(ct_block))]
                    if i == len(ct_block)/16-1:  # rm padding
                        pt_block_bytes = pt_block_bytes[:-pt_block_bytes[-1]]
                    pt += ''.join([chr(c) for c in pt_block_bytes])
        elif self.mode == 'CTR':
            '''
            IV  c0       c1
                ⊕        ⊕
                E(k,IV)   E(k,IV+1)
                m0       m1
            '''
            encryptor = self.cipher.encryptor()
            iv = int(ct[:32], 16)
            for i in range(0, len(ct_bytes), 16):
                ct_block = ct_bytes[i:i+16]
                pt_block_bytes = [a ^ b for (a, b) in zip(
                    ct_block, encryptor.update(
                        bytes.fromhex(hex(iv+int(i/16))[2:]))[:len(ct_block)])]
                pt += ''.join([chr(c) for c in pt_block_bytes])
        return pt


CBC_cts = (('140b41b22a29beb4061bda66b6747e14',
            '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2'
            'e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'),
           ('140b41b22a29beb4061bda66b6747e14',
            '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e'
            '713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'))
for (key, ct) in CBC_cts:
    aes = AES(key, 'CBC')
    print(aes.decrypt(ct))

CTR_cts = (('36f18357be4dbd77f050515c73fcf9f2',
            '69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc38'
            '8d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f'
            '51eeca32eabedd9afa9329'),
           ('36f18357be4dbd77f050515c73fcf9f2',
            '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0'
            'e311bde9d4e01726d3184c34451'))
for (key, ct) in CTR_cts:
    aes = AES(key, 'CTR')
    print(aes.decrypt(ct))
