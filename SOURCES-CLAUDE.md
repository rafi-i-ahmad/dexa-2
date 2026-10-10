# Sources

✓ = abstract, record or page checked on 2026-10-10. The other entries were carried over from the generated starter and haven't been re-checked.

## Competitors and context

- ✓ [EchoMRI systems](https://echomri.com/systems/): human 250K, 80K and 12K models; fat, lean, free and total water; 0.5-3.2 min scans. Manufacturer claims, and no price is listed.
- [Napolitano et al. 2008, QMR validation in humans](https://pubmed.ncbi.nlm.nih.gov/18223634/): repeatability and bias of an early prototype.
- [Galgani et al. 2011, EchoMRI-AH vs DXA](https://pubmed.ncbi.nlm.nih.gov/21224826/): similar one-week fat-mass precision.
- [Hologic Horizon DXA](https://www.hologic.com/horizondxa): body-composition acquisition advertised as taking as little as 2 min, with regional outputs.
- ✓ (title and listing only; full record not reachable) [West et al. 2016, MR body composition in large population studies](https://www.ukbiobank.ac.uk/publications/feasibility-of-mr-based-body-composition-analysis-in-large-scale-population-studies/): Dixon-based neck-to-knee analysis in UK Biobank.

## Low-field fat-water imaging

- ✓ [Dixon 1984, Simple proton spectroscopic imaging](https://pubmed.ncbi.nlm.nih.gov/6089263/): water and fat images from a modified spin echo at 0.35 T.
- ✓ [Liver PDFF at 0.55 T vs 3 T, pilot in patients](https://pmc.ncbi.nlm.nih.gov/articles/PMC12638424): good agreement with 3 T.
- ✓ [Liver PDFF at 0.55 T with locally low-rank deep-learning reconstruction](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12620156/), with the [ISMRM 2025 abstract](https://archive.ismrm.org/2025/0810.html) reporting a several-fold better reproducibility coefficient.
- ✓ [0.55 T spiral Dixon and denoising work](https://par.nsf.gov/search/author:%22Tasdelen,%20Bilal%22): concomitant-field correction and validated acquisition choices.
- ✓ [Simultaneous T1, T2 and fat fraction mapping at 0.55 T](https://repositorio-az.uc.cl/dspace/items/aa605299-bd44-4c8e-8646-e624aecf5df8): the authors say in-vivo PDFF accuracy still needs work.
- ✓ Wan et al. 2026, *Efficient water-fat separation for extremity MRI at ultra-low field (0.05 T)*, Acad Radiol 33:2128 (PMID 41692663). Two-point Dixon with T2\* correction, about 13 min in vivo. A corrigendum (PMID 42161740) exists, and its contents are unread.

## J-coupling

- ✓ [Uche & Galiana 2019, Distinguishing lipid subtypes by amplifying contrast from J-coupling](https://www.nature.com/articles/s41598-019-39780-4): non-uniform echo trains at **3 T only**, with two human subjects. It does not separate fat amount from lipid type.
- [Stokes et al. 2013, Enhanced refocusing of fat signals using optimised multipulse echo sequences](https://pmc.ncbi.nlm.nih.gov/articles/PMC3460031/): fat echo dynamics depend on coupling, shifts and timing.

## Magnets and hardware

- ✓ Tewari, O'Reilly & Webb 2021, J Magn Reson 324:106923 (PMID 33567389). Optimising magnet angles in discrete Halbach arrays improved homogeneity by about 17% for very short magnets, falling to about 5% above a length-to-radius ratio of about 3. A variable-diameter design with a ratio of about 4 improved by about 18%. That is useful, but it is nowhere near the orders of magnitude a 0.5 m body magnet would need.
- [O'Reilly et al. 2020, 50 mT Halbach brain and extremity MRI](https://arxiv.org/abs/2005.02834): a 27 cm bore and a magnet of about 75 kg.
- [Liu et al. 2021, 55 mT shielding-free brain MRI](https://www.nature.com/articles/s41467-021-27317-1): a samarium-cobalt magnet of about 750 kg.
- [Arnold N42H datasheet](https://www.arnoldmagnetics.com/wp-content/uploads/2017/11/N42H-151021.pdf): Br about 1.3 T, density 7,600 kg/m³, Br temperature coefficient about -0.12 %/°C.

## Sequence design, calibration and tools

- ✓ [MRzero, automated sequence discovery](https://open.fau.de/handle/openfau/16634): differentiable Bloch simulation with Pulseq export.
- [PyPulseq](https://github.com/pulseq/pypulseq) and [Spinach](https://spindynamics.org/wiki/index.php?title=Optimal_control_module).
- ✓ [Hernando et al. 2017, multisite and multivendor PDFF phantom study](https://pubmed.ncbi.nlm.nih.gov/27080068/): bias 0.22% and R² > 0.995. The [data is on Zenodo](https://zenodo.org/record/48266).
- ✓ [UW quantitative MR phantoms](https://qiml.radiology.wisc.edu/research/quantitative-mr-phantoms/).
