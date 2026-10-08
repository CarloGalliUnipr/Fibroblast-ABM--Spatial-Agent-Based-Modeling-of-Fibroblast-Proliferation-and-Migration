# NetLogo Interface setup

The source file assumes that the following names are created as Interface widgets. NetLogo makes widget variables global automatically, so do not also declare these names in `globals`.

## Required widgets

### Buttons

**setup**
- Command: `setup`
- Forever: off

**go**
- Command: `go`
- Forever: on

Optional screening buttons:

**screen-by-FBS**
- Command: `screen-by-FBS`

**screen-by-migration**
- Command: `screen-by-migration`

### Slider: `FBS`
Suggested values:
- Minimum: 0
- Maximum: 10
- Increment: 0.5
- Example default: 10
- Units: % FBS

### Slider: `migration`
Suggested values:
- Minimum: 0
- Maximum: 1
- Increment: 0.1
- Example default: 0.5
- Interpretation: dimensionless NetLogo displacement multiplier; with 1 patch = 20 µm, `migration = 1` corresponds to a nominal 20 µm/h before modifiers.

### Slider or input box: `initial-passage`
Suggested values:
- Minimum: 0
- Maximum: 30
- Increment: 1
- Example default: 5

### Slider or input box: `initial-cell-density`
This name is historical. The source currently uses it as the integer number of initial fibroblast agents.

Suggested values depend on world size and desired experiment. A typical example is 1000.

### Chooser: `treatment`
Choices must match the source code exactly:

```text
"Control" "Polynucleotides" "Newest" "Newest_half" "HA"
```

## Suggested monitors

- Cell count: `count turtles`
- Minimum population passage: `global-passage`
- Mean senescence factor: `average-senescence`
- Time: `ticks`

## Suggested plot

A simple population plot can use:

- x-axis: `ticks`
- y-axis: `count turtles`

Update command:

```netlogo
plot count turtles
```

## World settings

The biological meaning of one patch depends on the chosen calibration. The analysis workflow currently assumes 1 patch = 20 µm. The exact world dimensions should therefore be documented in the final manuscript and kept fixed across comparative simulation conditions.

## Reproducibility

For deterministic replication of stochastic runs, set the random seed before calling `setup`, e.g.

```netlogo
random-seed 12345
setup
```

For inferential analyses, use multiple independent random seeds per condition.
