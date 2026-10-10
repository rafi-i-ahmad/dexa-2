# Physics notes

These notes are condensed from our discussions. Wherever a number below comes from one of the scripts, the notes name the script.

## 1. Why one scanner can do so much

The hardware does only three things. $B_0$ lines up a tiny net magnetisation, RF pulses tip it over, and gradient coils make the precession frequency depend on position. The **pulse sequence** decides everything else: which pulses, the delays between them, and when to listen. Together those choose which physical process dominates the signal.

Tipped magnetisation relaxes in two independent ways:

- $T_1$ is the time constant for regrowth along $B_0$.
- $T_2$ is the time constant for the precessing signal to decay as spins drift out of phase.

For a spin echo, the signal is

$$S \propto \rho\left(1-e^{-TR/T_1}\right)e^{-TE/T_2}$$

Here $\rho$ is the proton density, $TR$ (repetition time) sets how much $T_1$ recovery happens between excitations, and $TE$ (echo time) sets how much $T_2$ decay happens before the signal is read.

**Worked example at 1.5 T.** Take fat with $T_1\approx260$ ms and $T_2\approx80$ ms, and cerebrospinal fluid (CSF, essentially water) with $T_1\approx4000$ ms and $T_2\approx2000$ ms.

- With TR = 500 ms and TE ≈ 10 ms: fat gives $1-e^{-500/260}=0.85$ and CSF gives $0.12$. Fat is about 7 times brighter, which is T1 weighting.
- With TR = 4000 ms and TE = 100 ms: fat gives $0.29$ and CSF gives $0.60$. CSF is now about twice as bright as fat, which is T2 weighting.

The spins are the same; only two timing numbers changed.

The same idea extends to other contrasts:

- diffusion, using opposed gradient pulses;
- inversion pulses that null one $T_1$;
- chemical shift;
- flow;
- magnetisation transfer;
- susceptibility.

The hardware sets the ceiling, for example gradient strength for diffusion and field uniformity for spectroscopy.

## 2. Fat-water separation at low field

**Chemical shift.** Electrons around each nucleus partly shield it from $B_0$, so a proton precesses at $\gamma B_0(1-\sigma)$. The shielding $\sigma$ is a fixed fraction, so shifts are quoted in ppm while their size in Hz scales with $B_0$. Fat's main peak (CH2, at 1.3 ppm) sits 3.4 ppm below water (4.7 ppm). Real fat has 6-10 peaks, so quantitative work uses a multi-peak model.

| $B_0$ | Fat-water shift | First opposed phase | First in phase |
|---|---|---|---|
| 0.1 T | 14.5 Hz | 34.5 ms | 69.1 ms |
| 0.25 T | 36.2 Hz | 13.8 ms | 27.6 ms |
| 0.5 T | 72.4 Hz | 6.9 ms | 13.8 ms |
| 1.5 T | 217 Hz | 2.3 ms | 4.6 ms |

Dixon invented the method at 0.35 T in 1984. It used a modified spin echo whose readout was offset from the true spin echo, so that fat and water were out of phase. Liver PDFF at 0.55 T has been shown to agree well with 3 T in patients.

Several issues are specific to low field and permanent magnets:

- **Use spin-echo or turbo-spin-echo Dixon.** In a permanent magnet, $T_2^*$ is set by the magnet's non-uniformity. With a spin echo shifted by $\tau$, only that shift builds up off-resonance phase, and everything else is refocused.
- **Smooth vs local field errors.** A field map handles smooth $B_0$ variation across the image. However, the field spread *inside one voxel* must be well below the fat-water shift itself, 3.4 ppm. Otherwise fat and water overlap within the voxel and no fit can separate them. Linear field errors can be cancelled with gradient-coil offsets, but higher-order errors need passive shims or a better magnet.
- **Temperature.** NdFeB loses about 0.12% of its field per °C. At 0.25 T that is about 12.8 kHz per °C, compared with a 36 Hz fat-water shift.

Beyond a multi-peak fat model and a field map, a confounder-corrected fit also handles:

- $R_2^*=1/T_2^*$ decay, fitted together with the fat and water amplitudes.
- **$T_1$ bias.** Fat recovers faster than water, so use a small flip angle or correct with measured $T_1$.
- **Magnitude noise bias.** At low SNR the magnitude of a noisy signal is biased upwards, so 0% fat reads as a few per cent. Fitting complex data avoids this, and it is probably the most important correction at low field.
- **Phase errors** from eddy currents and concomitant fields. Concomitant fields scale roughly as $G^2/B_0$, so they get worse as the field drops.
- **Fat-water swaps.** An error of one fat-water shift in the field map gives the same data with the labels swapped. Smoothness priors such as region growing and graph cuts resolve this.
- **Echo-time choice**, by minimising the Cramér-Rao lower bound. That bound is the best precision any unbiased fit could reach, so minimising it picks the most informative echo times.
- **Regularised reconstruction**, which at 0.55 T has improved PDFF reproducibility several-fold. One example is locally low-rank regularisation with deep learning.
- **Joint relaxometry**, mapping $T_1$, $T_2$ and fat fraction together.

Relaxation and diffusion contrast, which is what QMR uses, needs no spectral resolution. That makes it the most field-robust tool available. Fat has a different $T_2$ from water and diffuses far more slowly.

## 3. J-coupling

**Why it is called field-independent.** Proton A's nuclear moment slightly polarises the bonding electrons, which pass a small field on to proton B. A's moment is fixed, and either "up" or "down", so B's frequency moves by $\pm J/2$ Hz at any $B_0$. Chemical shift, by contrast, is driven by $B_0$ and so scales with it.

**Why it can still be invisible.** The coupling energy $hJ\,\mathbf{I}_A\cdot\mathbf{I}_B$ depends only on the angle between the two spins. Uniform pulses, equal precession rates and detection of the total magnetisation never change that angle, so the coupling never shows up in the signal. In quantum terms, $\mathbf{I}_A\cdot\mathbf{I}_B$ commutes with total-spin rotations. This is why water's two protons show no J effect. Seeing J needs a chemical-shift difference $\Delta\nu$ between the coupled protons, and $\Delta\nu$ in Hz scales with $B_0$.

**Its one real advantage.** J survives a spin echo. A 180° pulse flips each spin's phase *and* its partner's state, so the J phase keeps accumulating while field errors and chemical shift refocus. In principle, therefore, J-based contrast tolerates a magnet that is too non-uniform for Dixon. This is the honest motivation for testing it.

**What `sims/j_echo.py` shows.** The script uses exact density matrices, ideal pulses, no relaxation and J = 7 Hz throughout. Modulation depth is 1 for clean textbook modulation.

| Fragment | 0.1 T | 0.25 T | 0.5 T | 1.5 T | 3 T |
|---|---|---|---|---|---|
| Bare pair 0.4 ppm apart (2 spins) | 0.07 | 0.65 | 0.85 | 0.99 | 1.00 |
| Fat chain end CH3-CH2-CH2 (7 spins) | 0.02 | 0.18 | 0.42 | 0.50 | 0.53 |
| CH2(1.3)-CH2(2.0)-CH=(5.3) (5 spins) | 0.50 | 0.50 | 0.55 | 0.56 | 0.52 |

There are two lessons:

1. **Strong coupling depends on the whole coupling network, not on one $\Delta\nu/J$ ratio.** A bare pair still keeps most of its modulation at 0.25 T. The real chain end, where each proton couples to several partners, loses about two-thirds of its high-field modulation. Reasoning from a single pair is too optimistic.
2. **What survives at low field is mostly a lipid-type signal.** The double-bond and allylic protons are 3.3 ppm apart, about the same as the fat-water shift, so their coupling survives at low field for the same reason Dixon does. But they are a small minority of fat's protons, and how many there are depends on how unsaturated the fat is. A J signal at 0.25 T therefore reports lipid composition as much as fat amount. All published J-based lipid contrast so far is at 3 T (Uche & Galiana 2019).

There are two further practical costs. First, a 7 Hz effect needs 100-400 ms to develop, while fat's $T_2$ is around 100 ms or less. Second, rapid echo trains suppress J evolution altogether, which is why fat looks bright on fast spin echo.

**Where J really earns its keep:**

- High-field spectroscopy editing, for example lactate inverting at TE = 1/J ≈ 144 ms, or GABA with MEGA-PRESS.
- Proton-carbon-13 coupling (J ≈ 125-145 Hz, always weakly coupled), although carbon-13 is only about 1% of carbon.
- Parahydrogen hyperpolarisation, where near-equivalent spins store hidden order that a reaction releases.

**Verdict.** J is not a replacement for chemical shift at 0.25 T. At best it is a secondary measurement in a hybrid, and it is most interesting exactly where the magnet is too non-uniform for Dixon.

## 4. How complete can a simulator be?

The physics is essentially complete at these energies: the spin Hamiltonian plus classical electromagnetism. A simulator is limited by other things:

- **Compute.** $N$ coupled spins need a $2^N\times2^N$ density matrix. A triglyceride has about 100 protons, so it has to be split into fragments, as `j_echo.py` does.
- **The sample.** Tissue $T_1$ and $T_2$ emerge from microstructure and water exchange that you never know voxel by voxel, so you fit effective or two-pool parameters.
- **Your hardware.** Field maps, B1 non-uniformity, gradient non-linearity, eddy currents and concomitant fields can all be modelled, but each must be measured on your own magnet. These are usually the largest errors.
- **The subject.** Breathing, heartbeat, flow and temperature.
- **Thermal noise.** This is the irreducible part: you can model its statistics exactly but never its particular values in a given scan.

Rule of thumb: add a model term only when its effect exceeds your noise-limited precision, and use phantoms (where the truth is known) to catch what the model misses. A sensible stack is a Bloch simulator for imaging (KomaMRI or JEMRIS), a small density-matrix module for J (Spinach, or `j_echo.py`), measured field maps, and complex Gaussian noise.

## 5. Sequence design and ML

Most design work runs from theory to simulation to tuning on phantoms. The theory includes the Bloch equations, the Ernst angle (the flip angle that maximises signal for a given $T_1$ and TR) and Cramér-Rao bounds. RF pulses themselves are designed with Shinnar-Le Roux or optimal control.

Automated design exists too:

- **MRzero** optimises the sequence by gradient descent through a differentiable end-to-end Bloch simulation, then exports the result through Pulseq.
- **MR fingerprinting** varies sequence parameters pseudo-randomly and matches each voxel's signal against a simulated dictionary.
- **Learned k-space sampling** trains the sampling pattern together with the reconstruction.

The catch is that an optimiser exploits whatever the simulator gets wrong. A plain Bloch simulator has no J-coupling, for instance. Hold out whole lipid mixtures and hardware conditions, compare any learned estimator with a plain model fit, and test whether it shrinks real changes towards average values.

## 6. Calibration

**Per scan:** centre frequency, transmit gain (so a nominal 90° pulse is 90°), shimming and a field map.

**Phantoms:**

- Oil-water emulsion vials spanning 0-100% PDFF. The multisite study found 0.22% bias and R² > 0.995 across vendors and fields, and its raw data is public.
- The ISMRM/NIST system phantom: NiCl2-doped spheres for $T_1$, MnCl2-doped spheres for $T_2$, proton-density spheres and geometry markers. Doped water in vials is the DIY version.
- Diffusion phantoms and fat-iron-fibrosis phantoms for later stages.

**In vivo:** single-voxel MR spectroscopy is the usual PDFF reference, with biopsy behind it. A comparison scan on a 1.5 or 3 T system is the pragmatic check.

## 7. How much physics is needed

**Layer 1** is the classical picture: the Bloch equations (coupled linear ODEs), the rotating frame, the Fourier transform and phase bookkeeping. It covers imaging, Dixon, QMR and most viability questions.

**Layer 2** is density matrices and product operators, which is where J-coupling properly lives. It needs first-year linear algebra; the difficulty is conceptual.

**Reading:** Hornak, *The Basics of MRI* (free online); McRobbie et al., *MRI from Picture to Proton*; Keeler, *Understanding NMR Spectroscopy*.
