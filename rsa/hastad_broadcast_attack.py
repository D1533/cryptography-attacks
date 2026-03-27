#!/usr/bin/env python3

from sage.all import *
from Crypto.Util.number import bytes_to_long
from gmpy2 import iroot

def generate_rsa_key(e):
    while True:
        p = int(random_prime(2**512))
        q = int(random_prime(2**512))
        phi = (p-1)*(q-1) 
        if gcd(e, phi) == 1:
            N = p*q
            d = pow(e, -1, phi)
            return N, d

def hastad_broadcast_attack(ciphertexts, moduli, e):
    m = crt(ciphertexts, moduli)
    m, exact = iroot(m, e)
    if exact:
        return m
    return None


# --- Setup ---
e = 3 
m = bytes_to_long(os.urandom(16))
ciphertexts = []
moduli = []
for _ in range(e):
    N, d = generate_rsa_key(e)
    moduli.append(N)
    ciphertexts.append(pow(m, e, N))

# --- PoC - Hastad's Broadcast Attack ---
m_recovered = hastad_broadcast_attack(ciphertexts, moduli, e)
assert(m_recovered == m)


