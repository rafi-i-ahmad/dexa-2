# dexa-2
A potential MRI based competitor to dual-energy X-ray absorptiometry (DEXA) scans.

## main-question

Could a dedicated low-field permanent-magnet (most are superconducting) MRI machine measure regional body composition well enough, quickly enough and cheaply enough to be worth manufacturing?

If yeah, stonks.

## how-dexa-works

DEXA uses two X-rays of differing energies to basically solve a 2x2 linear system of equations all across the body. By knowing the absorption coefficient for bone and/or lean mass it can work out how much of each is present. Still not 100% sure how it works out composition for >2 layers? 

I might put the how the other technologies work in more detail elsewhere to not clutter stuff.

## competitors 

from claude:

| Option | What it gives | Weaknesses |
|---|---|---|
| DXA | Bone density (the clinical standard), regional fat and lean, a scan of a few minutes, tiny X-ray dose | A 2D projection, so visceral fat is modelled rather than seen; "lean" includes water and assumes constant hydration |
| QMR (EchoMRI) | Whole-body fat, lean, free water and total water in 0.5-3.2 min, no radiation | No spatial information, no bone |
| Existing MRI (1.5/3 T, or 0.55 T) with automated analysis | Visceral vs subcutaneous fat, muscle volumes, muscle fat infiltration, liver PDFF; already run at UK Biobank scale | Scanner cost and access |
| This project | Hoping the existing-MRI outputs from a cheaper dedicated machine | A bit f*cking crazy to try and build |

we have an advantage of something that doesn't need ultra-high field strength for smth like brain scanning. As well as not really being something life or death.

## Plan

* Get some targets we'd need to hit like cost, quality etc. In particular we need to probably check if we even find this interesting enough to pursue. The physics required is pretty damn complex and it's a medical product I have no clue what regulation + approval times look like even we make a perfect revolutionary product.
* Decide if we'd want to just manafacture or setup clincs
* Work out who would even buy this stuff
* Work out magnet strength (I think 0.2-0.5T) 
	* Work out the magnet technology (I suggest perm magnet) 
	* Decide on magnet length, I suggest we try to optimise for thinness (not too short otherwise end effects are mad)
* Start actually vibe-physicsing and do first small experiments. Though these will be software experiments first.
