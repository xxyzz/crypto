# Week 5 - Programming Assignment

Your goal this week is to write a program to compute discrete log modulo a prime *p*. Let *g* be some element in ℤₚ<sup>\*</sup> and suppose you are given *h* in ℤₚ<sup>\*</sup> such that *h* = *g<sup>x</sup>* when 1 ≤ *x* ≤ 2<sup>40</sup>. Your goal is to find *x*. More precisely, the input to your program is *p*, *g*, *h* and the output is *x*.

The trivial algorithm for this problem is to try all 2<sup>40</sup> possible values of *x* until the correct one is found, that is until we find an *x* satisfying *h* = *g<sup>x</sup>* in ℤₚ. This requires 2<sup>40</sup> multiplications. In this project you will implement an algorithm that runs in time roughly √2<sup>40</sup> = 2<sup>20</sup> using a meet in the middle attack.

Let *B* = 2<sup>20</sup>. Since *x* is less than *B²*.

we can write the unknown *x* base *B* as *x* = *x₀B* + *x₁*

where *x₀*, *x₁* are in the range \[0, *B* - 1\]. Then

*h* = *g<sup>x</sup>* = *g<sup>x₀B + x₁</sup>* =(*g<sup>B</sup>*)<sup>*x₀*</sup> ⋅ *g<sup>x₁</sup>* in ℤₚ.

By moving the term *g<sup>x₁</sup>* to the other side we obtain

*h/g<sup>x₁</sup>* = (*g<sup>B</sup>*)<sup>*x₀*</sup> in ℤₚ.

The variables in this equation are *x₀*, *x₁* and everything else is known: you are given *g*, *h* and *B* = 2<sup>20</sup>. Since the variables *x₀* and *x₁* are now on different sides of the equation we can find a solution using meet in the middle([Lecture 3.3](https://www.coursera.org/learn/crypto/lecture/fPA8S/exhaustive-search-attacks) at 14:25):

- First build a hash table of all possible values of the left hand side *h/g<sup>x₁</sup>* for *x₁* = 0, 1, ..., 2<sup>20</sup>.

- Then for each value *x₀* = 0, 1, 2, ..., 2<sup>20</sup>. check if the right hand side (*g<sup>B</sup>*)<sup>*x₀*</sup> is in this hash table. If so, then you have found a solution (*x₀*, *x₁*) from which you can compute the required *x* as *x* = *x₀B* + *x₁*.

The overall work is about 2<sup>20</sup> multiplications to build the table and another 2<sup>20</sup> lookups in this table.

Now that we have an algorithm, here is the problem to solve:

```
p = 134078079299425970995740249982058461274793658205923933 \
    77723561443721764030073546976801874298166903427690031 \
    858186486050853753882811946569946433649006084171

g = 11717829880366207009516117596335367088558084999998952205 \
    59997945906392949973658374667057217647146031292859482967 \
    5428279466566527115212748467589894601965568

h = 323947510405045044356526437872806578864909752095244 \
    952783479245297198197614329255807385693795855318053 \
    2878928001494706097394108577585732452307673444020333
```

Each of these three numbers is about 153 digits. Find *x* such that *h* = *g<sup>x</sup>* in ℤₚ.

To solve this assignment it is best to use an environment that supports multi-precision and modular arithmetic. In Python you could use the [gmpy2](https://gmpy2.readthedocs.io/en/latest/mpz.html#mpz-methods) or [numbthy](https://github.com/Robert-Campbell-256/Number-Theory-Python/blob/master/numbthy.py) modules. Both can be used for modular inversion and exponentiation. In C you can use [GMP](https://gmplib.org). In Java use a BigInteger class which can perform mod, modPow and modInverse operations.
