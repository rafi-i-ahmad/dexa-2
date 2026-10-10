"""How far a finite-length Halbach cylinder is from the ideal formula B0 = Br ln(ro/ri).

Ideal, continuously magnetised dipole Halbach; no discrete blocks, end rings,
shims or temperature effects. Treat the output as a lower bound on how hard
the magnet problem is, not as a design.

Method (magnetic charges): magnetisation at angle 2*phi gives volume charge
-2 M0 cos(phi)/r, surface charge +M0 cos(phi) outside and -M0 cos(phi) inside,
none on the end faces. Each (r, phi) column is a uniform line segment along z
with a closed-form field, so only a 2D sum is needed. selfcheck() compares it
with the infinite-length formula and with an independent dipole sum.

Run:  python sims/halbach.py [--field 0.25] [--bore 0.8]
"""
import argparse

import numpy as np
from scipy.optimize import brentq

BR, DENSITY = 1.3, 7600.0  # N42-class NdFeB: remanence (T), density (kg/m^3)


def field(points, ri, ro, L, br=BR, n_phi=720, n_r=120):
    """Flux density (T) at points (N, 3) in metres; axis along z, centred at the origin."""
    p = np.atleast_2d(np.asarray(points, float))
    dphi, dr = 2 * np.pi / n_phi, (ro - ri) / n_r
    phi = (np.arange(n_phi) + 0.5) * dphi
    r = ri + (np.arange(n_r) + 0.5) * dr
    R, P = np.meshgrid(r, phi, indexing="ij")
    xy = np.concatenate([np.stack([R * np.cos(P), R * np.sin(P)], -1).reshape(-1, 2),
                         np.stack([ro * np.cos(phi), ro * np.sin(phi)], -1),
                         np.stack([ri * np.cos(phi), ri * np.sin(phi)], -1)])
    lam = np.concatenate([(-2 * np.cos(P) * dr * dphi).ravel(),
                          np.cos(phi) * ro * dphi,
                          -np.cos(phi) * ri * dphi])
    out = np.empty_like(p)
    for i, (x, y, z) in enumerate(p):
        dx, dy = x - xy[:, 0], y - xy[:, 1]
        d2 = dx * dx + dy * dy
        s1, s2 = -L / 2 - z, L / 2 - z
        q1, q2 = np.sqrt(d2 + s1 * s1), np.sqrt(d2 + s2 * s2)
        perp = lam * (s2 / q2 - s1 / q1) / d2
        out[i] = perp @ dx, perp @ dy, lam @ (1 / q2 - 1 / q1)
    return br / (4 * np.pi) * out


def dipole_sum(point, ri, ro, L, br=BR, n=(24, 360, 100)):
    """Independent check: sum point-dipole fields over volume cells."""
    nr, nphi, nz = n
    r = ri + (np.arange(nr) + 0.5) * (ro - ri) / nr
    phi = (np.arange(nphi) + 0.5) * 2 * np.pi / nphi
    z = -L / 2 + (np.arange(nz) + 0.5) * L / nz
    R, P, Z = np.meshgrid(r, phi, z, indexing="ij")
    w = (R * (ro - ri) / nr * 2 * np.pi / nphi * L / nz).ravel()
    pos = np.stack([R * np.cos(P), R * np.sin(P), Z], -1).reshape(-1, 3)
    m = np.stack([np.cos(2 * P), np.sin(2 * P), 0 * P], -1).reshape(-1, 3)
    d = np.asarray(point, float) - pos
    dist = np.linalg.norm(d, axis=1)
    u = d / dist[:, None]
    mu = np.sum(m * u, axis=1)
    return br / (4 * np.pi) * np.sum(w[:, None] * (3 * mu[:, None] * u - m) / dist[:, None] ** 3, axis=0)


def region(diameter, length, n=9):
    """Points filling a cylinder: `diameter` across the bore, `length` along it."""
    a = np.linspace(-diameter / 2, diameter / 2, n)
    zs = np.linspace(-length / 2, length / 2, max(3, n // 2))
    return np.array([(x, y, z) for x in a for y in a for z in zs
                     if x * x + y * y <= (diameter / 2) ** 2 + 1e-12])


def spread_ppm(B):
    m = np.linalg.norm(B, axis=1)
    return (m.max() - m.min()) / m.mean() * 1e6


def max_gradient_mT_per_m(pts, ri, ro, L, h=1e-3):
    """Largest |grad |B|| over the points, by central differences."""
    g = []
    for p in pts:
        comps = []
        for k in range(3):
            e = np.zeros(3)
            e[k] = h
            b = np.linalg.norm(field([p + e, p - e], ri, ro, L), axis=1)
            comps.append((b[0] - b[1]) / (2 * h))
        g.append(np.linalg.norm(comps))
    return 1e3 * max(g)


def selfcheck():
    ri = 0.4
    ro = ri * np.exp(0.3 / BR)
    b_long = np.linalg.norm(field([(0, 0, 0)], ri, ro, L=200.0)[0])
    assert abs(b_long - 0.3) < 1e-3, b_long
    for pt in [(0, 0, 0), (0.2, 0, 0.1)]:
        a, b = field([pt], ri, ro, L=0.5)[0], dipole_sum(pt, ri, ro, L=0.5)
        assert np.allclose(a, b, atol=2e-4), (pt, a, b)
    print("selfcheck ok: long magnet matches Br ln(ro/ri); short magnet matches an independent dipole sum\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--field", type=float, default=0.25, help="target centre field, T")
    ap.add_argument("--bore", type=float, default=0.8, help="magnet inner diameter, m")
    args = ap.parse_args()
    selfcheck()
    b0, ri = args.field, args.bore / 2
    centre = lambda ro, L: np.linalg.norm(field([(0, 0, 0)], ri, ro, L, n_phi=360, n_r=200)[0])
    ro_ideal = ri * np.exp(b0 / BR)
    small, big = region(0.20, 0.20), region(0.45, 0.20)
    print(f"Target {b0} T, inner diameter {args.bore} m. Ideal formula: wall {100 * (ro_ideal - ri):.1f} cm.")
    print(f"{'length':>7} {'ideal wall gives':>17} {'wall for target':>16} {'NdFeB':>9} "
          f"{'spread 20x20 cm':>16} {'spread 45x20 cm':>16} {'max grad (20 cm)':>17}")
    for L in [0.5, 1.0, 1.5, 2.0]:
        ro = brentq(lambda x: centre(x, L) - b0, ri * 1.001, 4 * ri, xtol=1e-5)
        mass = DENSITY * np.pi * L * (ro ** 2 - ri ** 2)
        print(f"{L:6.1f}m {centre(ro_ideal, L):15.3f} T {100 * (ro - ri):13.1f} cm {mass:7,.0f} kg "
              f"{spread_ppm(field(small, ri, ro, L)):12,.0f} ppm {spread_ppm(field(big, ri, ro, L)):12,.0f} ppm "
              f"{max_gradient_mT_per_m(region(0.20, 0.20, 5), ri, ro, L):12.1f} mT/m")
    print("\nSpread = (max - min)/mean of |B| in a cylinder (diameter x length), before any shimming.")


if __name__ == "__main__":
    main()
