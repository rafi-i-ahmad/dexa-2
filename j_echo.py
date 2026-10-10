"""How much J-coupling modulation survives in a spin echo as B0 drops.

Exact density-matrix calculation for small groups of coupled protons, with ideal
hard 90x and 180y pulses and no relaxation. J is the same at every field; what
shrinks is the chemical-shift difference (in Hz) between the coupled protons.

"Modulation depth" = half the peak-to-peak swing of the normalised echo
amplitude over echo times 0 to 3/J. A weakly coupled pair gives 1.0
(the echo follows cos(pi J TE)); equivalent protons give 0.

Run:  python sims/j_echo.py      (a few seconds)
"""
from functools import reduce

import numpy as np

GAMMA = 42.577e6  # proton gyromagnetic ratio / 2pi, Hz/T
_s = {"x": np.array([[0, 1], [1, 0]]) / 2,
      "y": np.array([[0, -1j], [1j, 0]]) / 2,
      "z": np.array([[1, 0], [0, -1]]) / 2}


def _op(axis, k, n):
    return reduce(np.kron, [_s[axis] if i == k else np.eye(2) for i in range(n)])


def _rotation(op, angle):
    w, v = np.linalg.eigh(op)
    return v @ np.diag(np.exp(-1j * angle * w)) @ v.conj().T


def echo_curve(shifts_ppm, couplings, b0, tes):
    """Normalised echo amplitude at each TE. couplings = [(i, j, J_Hz), ...]."""
    n = len(shifts_ppm)
    X, Y, Z = ([_op(a, k, n) for k in range(n)] for a in "xyz")
    nu = np.array(shifts_ppm) * 1e-6 * GAMMA * b0
    nu -= nu.mean()  # rotating frame
    H = sum(2 * np.pi * nu[k] * Z[k] for k in range(n))
    for i, j, J in couplings:
        H = H + 2 * np.pi * J * (X[i] @ X[j] + Y[i] @ Y[j] + Z[i] @ Z[j])
    w, v = np.linalg.eigh(H)
    Ix, Iy, Iz = sum(X), sum(Y), sum(Z)
    p90, p180 = _rotation(Ix, np.pi / 2), _rotation(Iy, np.pi)
    rho0 = p90 @ Iz @ p90.conj().T
    detect = (Ix + 1j * Iy).conj().T
    s0 = np.trace(rho0 @ detect)
    out = []
    for t in tes:
        U = v @ np.diag(np.exp(-1j * w * t / 2)) @ v.conj().T
        rho = U @ rho0 @ U.conj().T
        rho = p180 @ rho @ p180.conj().T
        rho = U @ rho @ U.conj().T
        out.append(np.real(np.trace(rho @ detect) / s0))
    return np.array(out)


def depth(shifts, couplings, b0, J=7.0, n=241):
    c = echo_curve(shifts, couplings, b0, np.linspace(0, 3 / J, n))
    return (c.max() - c.min()) / 2


def selfcheck():
    J, tes = 7.0, np.array([0.05, 1 / 7.0, 0.3])
    pair = [(0, 1, J)]
    assert np.allclose(echo_curve([0.9, 1.3], [(0, 1, 0.0)], 0.25, tes), 1)  # shift alone is refocused
    assert np.allclose(echo_curve([1.3, 1.3], pair, 0.25, tes), 1)  # equivalent spins: J invisible
    weak = echo_curve([0.0, 1000.0], pair, 3.0, tes)  # huge shift difference: weak coupling
    assert np.allclose(weak, np.cos(np.pi * J * tes), atol=1e-3)
    print("selfcheck ok: refocusing, equivalent-spin and weak-coupling limits reproduced\n")


# Approximate fragments, J = 7 Hz between neighbouring groups (equivalent protons share a shift).
J = 7.0
FRAGMENTS = {
    "bare pair, 0.4 ppm apart (2 spins)":
        ([0.9, 1.3], [(0, 1, J)]),
    "fat chain end CH3-CH2-CH2 (7 spins)":
        ([0.9] * 3 + [1.3] * 4,
         [(i, j, J) for i in range(3) for j in (3, 4)] + [(i, j, J) for i in (3, 4) for j in (5, 6)]),
    "fat CH2(1.3)-CH2(2.0)-CH=(5.3) (5 spins)":
        ([1.3, 1.3, 2.0, 2.0, 5.3],
         [(i, j, J) for i in (0, 1) for j in (2, 3)] + [(i, 4, J) for i in (2, 3)]),
}

if __name__ == "__main__":
    selfcheck()
    fields = [0.1, 0.25, 0.5, 1.5, 3.0]
    print(f"{'J modulation depth':42s}" + "".join(f"{b:>7} T" for b in fields))
    for name, (shifts, couplings) in FRAGMENTS.items():
        print(f"{name:42s}" + "".join(f"{depth(shifts, couplings, b):9.2f}" for b in fields))
    print("\nNo relaxation modelled: fat T2 (about 100 ms or less) also eats into the 100-400 ms a 7 Hz effect needs.")
