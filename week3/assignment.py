#!/usr/bin/env python3

'''
    SHA256        SHA256         SHA256
h0<-------       -------        -------
          |     |       |      |       |
    ---------   |  ---------   | -------
    block0 h1 <--  block1 h2 <-- block 2

https://crypto.stanford.edu/~dabo/onlineCrypto/6.1.intro.mp4_download
https://crypto.stanford.edu/~dabo/onlineCrypto/6.2.birthday.mp4_download
'''

from pathlib import Path

from cryptography.hazmat.primitives import hashes

video_path = Path('6.1.intro.mp4_download')
ONE_KB = pow(2, 10)
with video_path.open('rb') as f:
    previous_hash = b''
    for i in range(video_path.stat().st_size // ONE_KB, -1, -1):
        f.seek(i * ONE_KB)
        digest = hashes.Hash(hashes.SHA256())
        if previous_hash == b'':
            digest.update(f.read())
        else:
            digest.update(f.read(ONE_KB) + previous_hash)
        previous_hash = digest.finalize()
    print(previous_hash.hex())
