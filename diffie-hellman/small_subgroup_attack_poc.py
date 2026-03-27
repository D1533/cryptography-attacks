#!/usr/bin/env python3

from sage.all import *

# --- Setup ---
p = random_prime(2**128)   

F_p = GF(p)
g = F_p.multiplicative_generator()

# Ensure order of g is small enough
factors = factor(p-1)
for q, e in factors[::-1]:
    if q < 2**20:
        g = pow(g, (p-1)//q, p)
        break

x = randint(2, g.multiplicative_order() - 1)
h = pow(g, x, p)

# --- PoC - Small Subgroup Attack
x_recovered = h.log(g)
assert(x_recovered == x)
