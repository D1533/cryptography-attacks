#!/usr/bin/env python3

from sage.all import *

def get_smooth_prime(n, primes_max_bit_size = 15):
    while True:
        N = 1
        for i in range(n):
            p_i = random_prime(2**primes_max_bit_size)
            e_i = randint(1, 5)
            N *= p_i**e_i
        
        p = N + 1
        if is_prime(p):
            return p

def pohlig_hellman_attack(h, g, p, max_bit_size):
    factors = factor(p-1)

    X = []
    moduli = []
    prod = 1
    for p_i, e_i in factors:
        prod *= p_i**e_i
        if int(prod).bit_length() > max_bit_size:
            break
        
        g_i = pow(g, (p-1)//(p_i**e_i), p)
        h_i = pow(h, (p-1)//(p_i**e_i), p)
        x_i = discrete_log(h_i, g_i, ord=p_i**e_i)
        X.append(x_i)
        moduli.append(p_i**e_i)

    x = crt(X, moduli)
    
    return x


# --- Setup ---
p = get_smooth_prime(10)

g = primitive_root(p)
x = randint(2, p-1)
h = pow(g, x, p)

# --- PoC - Pohlig Hellman Attack ---
x_recovered = pohlig_hellman_attack(h, g, p, 2**15)

assert(x == x_recovered)



