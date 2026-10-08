# Reproducibility and simulation practice

## Random seeds

The model is stochastic. For an exactly repeatable run, set a seed before calling `setup`:

```netlogo
random-seed 12345
setup
```

For scientific comparison among parameter combinations, use multiple independent seeds per condition. Report the number of replicates and how seeds were generated or assigned.

## Recommended output structure

For each replicate, store at minimum:

- treatment;
- FBS;
- migration setting;
- seed;
- tick;
- cell count.

If passage or nutrient-state analyses are important, also export mean passage, passage distribution, mean senescence factor, and summary statistics of the nutrient field.

## Parameter sweeps

The built-in `screen-by-FBS` and `screen-by-migration` procedures generate single stochastic trajectories per parameter setting. For publication-quality uncertainty estimates, wrap these conditions in replicate loops with different random seeds or use NetLogo BehaviorSpace.

## Population-level curve fitting

The Python logistic-analysis script treats the first observed count in each trajectory as fixed `N0` and estimates `r` and `K`. These fitted parameters summarize the trajectory; they are not identical to the cell-level `base-growth-rate` and no carrying capacity is explicitly imposed in the ABM.

## Versioning

Tag the exact repository commit used for manuscript analyses. If the model rules change after publication, preserve the published version as a release tag rather than overwriting it.

## Known modeling assumptions

1. FBS currently enters both directly in the proliferation propensity and indirectly through initial nutrient availability.
2. Nutrients do not diffuse or replenish.
3. The cell-cycle threshold is a minimum eligibility time; realized interdivision times are longer because division remains probabilistic afterward.
4. `initial-cell-density` is currently an absolute cell count despite its name.
5. `active?` is always true in the present implementation.
6. Local contact, paracrine, and migration-crowding radii and multipliers are phenomenological parameters.
