# dexa-2
A potential MRI based competitor to dual-energy X-ray absorptiometry (DEXA) scans.

actual name is pending like it's mini-mri tbh

## main-question

Could a dedicated low-field, perma magnet (most MRIs are superconducting) MRI measure regional body composition well enough and quickly enough and cheaply enough to justify costs.

If yeah, stonks.

### in-and-outs

In: a person lies on a table inside a roughly 0.Xx Tesla permanent magnet for about 10-15 minutes, maybe with a moving table or magnet, definitely no radiation (makes this good for long term studies, like DEXA is still probably too much radiation for say weekly usage), no preparation beyond removing metal. Operator input is minimal stuff like height, weight, position (we can 1 and 3 with camera systems).

Out: a report per visit with something like:

	• visceral (organ fat) and subcutaneous (above your muscle) fat volumes, by region (abdomen, thighs, arms)
	• skeletal muscle volume by region, plus fat infiltration into muscle
	• liver fat fraction (PDFF)
	• whole-body fat and lean totals
	• change since last visit with error bars
___

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

* We need to probably check if we even find this interesting enough to pursue. The physics required is pretty damn complex and it's a medical product I have no clue what regulation + approval times look like even we make a perfect revolutionary product.
* Decide if we'd want to just manafacture or setup clinics too
* Work out who would even buy this stuff
	* Get some targets we'd need to hit like cost, quality etc. For these buyers to find us competitive
* Work out magnet strength (I think 0.2-0.5T) 
	* Work out the magnet technology (I suggest perm magnet) 
	* Decide on magnet length, I suggest we try to optimise for thinness (not too short otherwise end effects are mad)
* Start actually vibe-physicsing and do first small experiments. Though these will be software experiments first.
