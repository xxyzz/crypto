#!/usr/bin/env python3

'''
Suppose you are told that the one time pad encryption of the message
"attack at dawn" is 09e1c5f70a65ac519458e7e53f36

(the plaintext letters are encoded as 8-bit ASCII and the given ciphertext
 is written in hex). What would be the one time pad encryption of the
 message "attack at dusk" under the same OTP key?
'''


def str_to_int(s):
    return int(s.encode().hex(), base=16)


key = str_to_int("attack at dawn") ^ 0x09e1c5f70a65ac519458e7e53f36

print(hex(str_to_int("attack at dusk") ^ key))
