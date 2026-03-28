#!/usr/bin/env python3

import os
from sage.all import *
from hashlib import sha1
from Crypto.Util.number import bytes_to_long, long_to_bytes
import random

def sign(m, d, G):
    q = G.order()
    k = random.getrandbits(128)
    r = int((k*G)[0])
    while r % q == 0:
        k = random.getrandbits(128)
        r = int((k*G)[0])

    h = bytes_to_long(sha1(m).digest())
    s = (pow(k,-1,q) * (h + r*d)) % q

    return (r, s)

def biased_nonce_attack(signatures, hashes, G, Q, q):
    assert(len(signatures) == len(hashes))
    a = []
    t = [] 
    for (r, s), h in zip(signatures, hashes):
        a.append( (pow(s, -1, q)*h) % q)
        t.append( (pow(s, -1, q)*r) % q)
    
    B = 2**128
    n = len(signatures)
    M = Matrix(QQ, n + 2, n + 2)
    for i in range(n):
        M[i, i] = q
    
    for i in range(n):
        M[n, i] = t[i]
    M[n, n] = B / q
    
    for i in range(n):
        M[n + 1, i] = a[i]
    M[n + 1, n + 1] = B
    
    L = M.LLL()
    
    r1 = signatures[0][0]
    s1 = signatures[0][1]
    h1 = hashes[0]
    for row in L:
        k1 = int(row[0])
        d = int((pow(r1, -1, q) * (k1*s1 - h1) ) % q)
        if d*G == Q:
            return d


# --- Setup ---
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
a = -3
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291

E = EllipticCurve(GF(p), [a, b])
G = E.gen(0)
q = G.order()
d = randint(2, q - 1) # private key
Q = d*G 

messages = [os.urandom(16) for i in range(3)]
signatures = [sign(m, d, G) for m in messages]

# --- PoC - Biased Nonce Attack ---
hashes = [bytes_to_long(sha1(m).digest()) for m in messages]
d_recovered = biased_nonce_attack(signatures, hashes, G, Q, q) 
assert(d_recovered == d)


