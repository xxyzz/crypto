#!/usr/bin/env python3

# dinosaurs with laser guns!
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AES():
    def __init__(self, key, mode):
        self.key = bytes.fromhex(key)
        self.mode = mode

    def encrypt(self, pt, nonce):
        if self.mode == 'CBC':
            pass

    def decrypt(self, ct):
        nonce = bytes.fromhex(ct)[:16]
        ct_bytes = bytes.fromhex(ct)[16:]
        pt = ''
        if self.mode == 'CBC':
            cipher = Cipher(algorithms.AES(self.key), modes.ECB())
            decryptor = cipher.decryptor()
            for i in range(0, len(ct_bytes), 16):
                ct_block = ct_bytes[i:i+16]
                if i == 0:
                    pt_block_bytes = [n ^ c for (n, c) in zip(
                        nonce, decryptor.update(ct_block))]
                    pt += ''.join([chr(c) for c in pt_block_bytes])
                else:
                    previous_ct = ct_bytes[i-16:i]
                    pt_block_bytes = [a ^ b for (a, b) in zip(
                        previous_ct, decryptor.update(ct_block))]
                    if i == len(ct_block)/16-1:  # rm padding
                        pt_block_bytes = pt_block_bytes[:-pt_block_bytes[-1]]
                    pt += ''.join([chr(c) for c in pt_block_bytes])
        return pt


aes = AES('140b41b22a29beb4061bda66b6747e14', 'CBC')
print(aes.decrypt('4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7'
                  '897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be0'
                  '28ad7c1d81'))
