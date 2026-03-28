#!/usr/bin/env python3

from sage.all import *

def Hlift(E, P, F):
    x, y = map(ZZ, P.xy())
    for p in E.lift_x(x, all=True):
        xx, yy = map(F, p.xy())
        if y == yy:
            return p

def Smart_Attack(E, G, P):
    assert(p == E.order())
    F_p = GF(p)
    Eqq = E.change_ring(QQ)
    Eqp = Eqq.change_ring(Qp(p))
    G = p*Hlift(Eqp, G, F_p)
    P = p*Hlift(Eqp, P, F_p)
    G_x, G_y = G.xy()
    P_x, P_y = P.xy()

    return int(F_p( (P_x / P_y) / (G_x / G_y)))


# --- Setup ---
p = 0xa15c4fb663a578d8b2496d3151a946119ee42695e18e13e90600192b1d0abdbb6f787f90c8d102ff88e284dd4526f5f6b6c980bf88f1d0490714b67e8a2a2b77
a = 0x5e009506fcc7eff573bc960d88638fe25e76a9b6c7caeea072a27dcd1fa46abb15b7b6210cf90caba982893ee2779669bac06e267013486b22ff3e24abae2d42
b = 0x2ce7d1ca4493b0977f088f6d30d9241f8048fdea112cc385b793bce953998caae680864a7d3aa437ea3ffd1441ca3fb352b0b710bb3f053e980e503be9a7fece

E = EllipticCurve(GF(p), [a, b])

G = E(3034712809375537908102988750113382444008758539448972750581525810900634243392172703684905257490982543775233630011707375189041302436945106395617312498769005, 4986645098582616415690074082237817624424333339074969364527548107042876175480894132576399611027847402879885574130125050842710052291870268101817275410204850)
b = randint(2, p-1)
B = b*G

# --- PoC - Smart's Attack ---
b = Smart_Attack(E, G, B)
assert(b*G == B)
