# Model variables and parameters

This document defines the state variables, environmental variables, control parameters, and derived quantities used in the fibroblast ABM.

## Agent-level state variables

### `passage`
Replicative passage or replicative age of an individual fibroblast. All cells are initialized from the Interface value `initial-passage`. Passage is incremented only after a successful cell division. The daughter inherits the parent's updated passage value.

### `active?`
Boolean flag controlling whether a cell executes migration, nutrient consumption, and proliferation logic. All initialized and newly created cells are currently assigned `true`, and no rule in the present model changes the flag to `false`. It is therefore an implementation hook for future extensions rather than an active regulatory mechanism in the current model.

### `base-growth-rate`
Treatment-specific baseline proliferation parameter. Current values are Control 0.0593, Polynucleotides 0.0629, Newest 0.0579, Newest_half 0.0503, and HA 0.0672. This is an agent-level baseline propensity and is not identical to a population-level logistic growth rate fitted to simulation output.

### `time-since-division`
Elapsed time in hours since the cell last divided. Because one tick equals one hour, the variable is incremented by one each tick. Initial values are randomized from 0 to 23 h to reduce synchronization of the starting population.

### `division-threshold`
Cell-specific minimum time required before division becomes eligible. It is sampled from a normal distribution with mean 24 h and standard deviation 5 h. Values below 1 h are replaced by 1 h. A new threshold is drawn independently after each successful division for both the parent and daughter.

## Patch-level state variable

### `nutrients`
Local nutrient/resource availability associated with a NetLogo patch. At initialization, every patch receives `FBS / 10`. Each active cell subtracts `nutrient-consumption-rate` from its current patch once per tick, with a lower bound of zero. The present model contains no nutrient diffusion or replenishment.

## Global/model-level parameter

### `nutrient-consumption-rate`
Amount of local nutrient removed by an active fibroblast per hour. Current value: 0.001 nutrient units per cell per tick. It is initialized for all treatment conditions.

## Interface variables

### `FBS`
Serum concentration expressed as percent FBS. The model uses the normalized factor `FBS / 10`. FBS enters the proliferation rule directly and also initializes patch nutrients, so the current implementation imposes two FBS-dependent contributions.

### `migration`
Baseline displacement parameter in NetLogo patch units per hour. Under the current interpretation, 1 patch corresponds to 20 µm; therefore `migration = 1` corresponds to a nominal 20 µm/h before passage, crowding, collision, and boundary effects.

### `initial-passage`
Initial replicative passage assigned to every newly created fibroblast at model setup.

### `initial-cell-density`
Despite its historical name, this variable is currently used as the absolute number of fibroblast agents created at initialization. It should therefore be described in the manuscript as initial cell number unless the model world area is explicitly used to convert it to a physical density.

### `treatment`
Categorical treatment selector. Valid values in the current source are `Control`, `Polynucleotides`, `Newest`, `Newest_half`, and `HA`. It determines the baseline proliferation parameter and display color.

## Derived biological modifiers

### Senescence factor `s(p)`

\[
s(p)=
\begin{cases}
1,&p<10\\
(30-p)/20,&10\le p<30\\
0,&p\ge30
\end{cases}
\]

The factor leaves proliferation unchanged below passage 10, decreases linearly between passages 10 and 30, and suppresses proliferation completely from passage 30 onward.

### Passage-dependent migration factor `m(p)`

\[
m(p)=
\begin{cases}
1,&p<20\\
(30-p)/10,&20\le p<30\\
0,&p\ge30
\end{cases}
\]

Motility is retained fully below passage 20, decreases linearly between passages 20 and 30, and reaches zero at passage 30.

### Contact-inhibition factor `C_i`
Let \(n_i^c\) be the number of other fibroblasts within 0.3 patches of cell \(i\):

\[
C_i=
\begin{cases}
0,&n_i^c>4\\
1,&n_i^c\le4
\end{cases}
\]

This is a phenomenological local crowding rule, not a directly measured biochemical constant.

### Paracrine-stimulation factor `P_i`
Let \(n_i^p\) be the number of other fibroblasts within 1 patch of cell \(i\):

\[
P_i=
\begin{cases}
0.1,&n_i^p=0\\
0.5,&n_i^p=1\\
1,&n_i^p\ge2
\end{cases}
\]

The larger neighborhood is intended to represent local neighbor-dependent support. Cells counted within the contact radius are also included in this 1-patch count.

### Crowding-dependent migration factor `q(η)`
Let \(\eta_i\) be the number of other fibroblasts within 0.5 patches:

\[
q(\eta)=
\begin{cases}
1,&\eta=0\\
0.6,&1\le\eta\le2\\
0.3,&3\le\eta\le4\\
0.1,&\eta>4
\end{cases}
\]

These coefficients are heuristic calibration parameters intended to encode reduced free migration in crowded regions.

## Effective proliferation propensity

For a proliferation-eligible cell \(i\),

\[
g_i(t)=r_i\left(\frac{FBS}{10}\right)s(p_i(t))C_i(t)P_i(t)n(x_i(t),y_i(t),t).
\]

Once `time-since-division >= division-threshold`, the model draws a uniform random number \(U_i\sim U(0,1)\). Division occurs if \(U_i<g_i(t)\).

The sampled cell-cycle threshold is therefore a minimum eligibility time rather than the realized interdivision time. The realized interval also includes the stochastic waiting period until a successful Bernoulli division event.

## Migration displacement

For cell \(i\), the attempted hourly displacement is

\[
d_i(t)=M\,m(p_i(t))\,q(\eta_i(t)),
\]

where \(M\) is the Interface parameter `migration`. With 1 patch = 20 µm,

\[
d_i^{\mu m}(t)=20M\,m(p_i(t))\,q(\eta_i(t)).
\]

Movement direction is randomized each hour. If the attempted final position is within 0.1 patches of another cell, the move is rejected and the old position is restored.

## Population-level quantities

### `global-passage`
Reporter returning the minimum passage represented in the population. It returns 0 if no cells are present.

### `average-senescence`
Reporter returning the mean senescence multiplier across all fibroblasts. It returns 0 for an empty population.

### Fitted logistic `r` and `K`
When logistic curves are fitted to ABM population trajectories, the fitted intrinsic growth rate and carrying capacity are emergent summary descriptors. They are not imposed model parameters and need not equal `base-growth-rate` or any explicit carrying-capacity value.
