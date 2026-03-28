#!/usr/bin/env python3

from sage.all import *

def get_embedding_degree(n, p):
    k = 1
    while p ** k % n != 1:
        k += 1
    return k

def MOV_attack(E, G, P):
    n = G.order()
    p = E.base_ring().order() 
    k = get_embedding_degree(n, p)

    EK = E.base_extend(GF(p**k)) 
    PK = EK(P)
    GK = EK(G)
    
    while True:
        Q = EK.random_point()
        m = Q.order()
        Q = (m // gcd(m, n))*Q
        g = GK.weil_pairing(Q, n)
        if g.multiplicative_order() == n:
            break
    
    h = PK.weil_pairing(Q, n)
    l = h.log(g)

    return int(l)

# --- Setup ---
p = random_prime(2**64)
while p % 4 != 3:
    p = random_prime(2**64)
a = -1
b = 0
E = EllipticCurve(GF(p), [a, b])

G = E.gen(0)
G = (G.order() //factor(G.order())[-1][0]) * G
b = randint(2, G.order()-1)
B = b*G

# --- PoC - MOV Attack --- 
b = MOV_attack(E, G, B)
assert(b*G == B)

