#!/usr/bin/env python3

from gmpy2 import isqrt, mpz

N = mpz(648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877)
sqrt_N = isqrt(N)

for i in range(1, 2 ** 19):
    A = sqrt_N + i
    x = isqrt(A ** 2 - N)
    p = A - x
    q = A + x
    if p * q == N:
        print(p)
        break