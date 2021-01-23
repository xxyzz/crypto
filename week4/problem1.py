#!/usr/bin/env python3

'''
An attacker intercepts the following ciphertext (hex encoded):

20814804c1767293b99f1d9cab3bc3e7 ac1e37bfb15599e5f40eef805488281d

He knows that the plaintext is the ASCII encoding of the message "Pay Bob 100$"
(excluding the quotes). He also knows that the cipher used is CBC encryption
with a random IV using AES as the underlying block cipher.

Show that the attacker can change the ciphertext so that it will decrypt to
"Pay Bob 500$". What is the resulting ciphertext (hex encoded)?

m0 = IV ⊕ D(k, c0)
IV' = IV ⊕ m0 ⊕ m0'
m0' = IV' ⊕ D(k, c0)
'''

iv = 0x20814804c1767293b99f1d9cab3bc3e7
pad = b'1' + (16 - 1 - len(b'Pay Bob 100$')) * b'0'
m0 = int((b'Pay Bob 100$' + pad).hex(), 16)
new_m0 = int((b'Pay Bob 500$' + pad).hex(), 16)
new_iv = iv ^ m0 ^ new_m0
print(hex(new_iv) + 'ac1e37bfb15599e5f40eef805488281d')
