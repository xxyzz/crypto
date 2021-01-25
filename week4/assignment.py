#!/usr/bin/env python3

import requests

TARGET = 'https://crypto-class.appspot.com/po?er='
CT = bytes.fromhex('f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714'
                   'c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37d'
                   'bf7035d5eeb4')
message_len = len(CT) - 16
# https://en.wikipedia.org/wiki/Letter_frequency
letters = 'etaoinshrdlcumwfgypbvkxjqz'
chars = ' ' + ''.join([letter + letter.upper() for letter in letters])


def query(i, g, pt):
    # discard rest ciphertext
    rest_ct_len = i // 16 * 16
    if i % 16 == 0:
        rest_ct_len = (i // 16 - 1) * 16
    ct = int.from_bytes(CT[:len(CT) - rest_ct_len], 'big')
    if i == 1:
        guess = int.from_bytes(g.to_bytes(1, 'big'), 'big')
    else:
        guess = int.from_bytes(chars[g].encode() + pt[:(i-1) % 16], 'big')
    pad_len = i % 16
    if pad_len == 0:
        pad_len = 16
    guess = guess ^ int.from_bytes(pad_len.to_bytes(1, 'big') * pad_len, 'big')
    guess = guess << (16 * 8)  # modify previous ciphertext block
    guess = ct ^ guess
    r = requests.get(TARGET + hex(guess)[2:])
    if r.status_code == 403 or r.status_code == 200:  # invalid pad
        if (i == 1 and i < 255) or (i > 1 and g < len(chars) - 1):
            return query(i, g+1, pt)
        else:
            print('damn: {} {} {}'.format(i, g, pt))
            return b''
    elif r.status_code == 404:
        if i == 1:
            pt = g.to_bytes(1, 'big') * g
            return query(g+1, 0, pt)
        else:
            pt = chars[g].encode() + pt
            print('{} {} {}'.format(i, g, pt))
            if i < message_len:
                return query(i+1, 0, pt)
            else:
                return pt[:-pt[-1]]  # rm pad
    return b''


print(query(1, 1, b''))
