# Manuscript-oriented model description

## Model overview

A spatially explicit agent-based model of human gingival fibroblast proliferation and migration was implemented in NetLogo. Individual fibroblasts were represented as autonomous agents moving in a continuous two-dimensional coordinate system overlaid on the NetLogo patch lattice. One simulation tick was interpreted as 1 h of biological time.

At each simulation step, cells updated their cell-cycle clock, attempted migration, consumed local nutrients, evaluated local proliferative modifiers, and, if cell-cycle eligible, underwent a stochastic division trial. No global logistic growth equation or imposed population carrying capacity was used. Instead, population saturation emerged from local contact inhibition, paracrine support, nutrient depletion, replicative senescence, crowding-dependent migration, collision avoidance, and finite space.

For cell \(i\), the state vector may be written as

\[
\mathbf{s}_i(t)=\left(x_i(t),y_i(t),p_i(t),a_i(t),r_i,\tau_i(t),\Delta_i\right),
\]

where \(x_i,y_i\) are spatial coordinates, \(p_i\) is passage number, \(a_i\) is activity status, \(r_i\) is the treatment-specific baseline proliferation parameter, \(\tau_i\) is time since the previous division, and \(\Delta_i\) is the stochastic division threshold.

## Treatment-specific proliferative capacity

Each fibroblast was assigned a baseline proliferation parameter according to treatment: Control 0.0593, Polynucleotides 0.0629, Newest 0.0579, Newest_half 0.0503, and HA 0.0672. This agent-level parameter was subsequently modified by serum availability, passage-dependent senescence, cell-cell interactions, and nutrient availability.

## Cell-cycle timing

Each cell possessed an elapsed-time variable \(\tau_i\) and an individual minimum division threshold \(\Delta_i\). Thresholds were sampled independently from a normal distribution with mean 24 h and standard deviation 5 h, with values below 1 h replaced by 1 h. Initial cell-cycle phases were desynchronized by assigning `time-since-division` values uniformly from 0 to 23 h.

A division attempt was permitted only if

\[
\tau_i(t)\ge\Delta_i.
\]

After division, both parent and daughter reset \(\tau_i\) to zero and independently sampled a new \(\Delta_i\). Because division remained probabilistic after the threshold was reached, the sampled threshold represented a minimum eligibility time rather than the exact interdivision interval.

## Replicative senescence

Passage-dependent loss of proliferative competence was represented by

\[
s(p)=
\begin{cases}
1,&p<10,\\
(30-p)/20,&10\le p<30,\\
0,&p\ge30.
\end{cases}
\]

Passage increased only after successful division. Cells below passage 10 retained full proliferative competence, whereas proliferation declined linearly between passages 10 and 30 and ceased at passage 30.

## Local cell-cell interactions

Short-range contact inhibition and broader paracrine support were represented as separate multiplicative effects. For contact inhibition, the number of other fibroblasts within 0.3 patches was counted. Proliferation was suppressed when more than four neighbors were present in this radius. The resulting factor was

\[
C_i(t)=
\begin{cases}
0,&n_i^c>4,\\
1,&n_i^c\le4.
\end{cases}
\]

Paracrine support was based on the number of other fibroblasts within a radius of 1 patch:

\[
P_i(t)=
\begin{cases}
0.1,&n_i^p=0,\\
0.5,&n_i^p=1,\\
1,&n_i^p\ge2.
\end{cases}
\]

The overall local cell-cell growth modifier was \(C_iP_i\). These rules were intentionally kept phenomenological and parsimonious; the radii and coefficients were chosen to encode qualitative local biological constraints rather than to claim directly measured microscopic constants.

## Nutrient field

Each NetLogo patch contained a scalar nutrient variable \(n(x,y,t)\). At model initialization,

\[
n(x,y,0)=\frac{FBS}{10}.
\]

Every active cell consumed 0.001 nutrient units from its current patch per hour, with the patch value constrained to remain non-negative. No nutrient diffusion or replenishment was included.

## Effective proliferation propensity

For a proliferation-eligible cell \(i\), the effective hourly division propensity was

\[
g_i(t)=r_i\left(\frac{FBS}{10}\right)s(p_i(t))C_i(t)P_i(t)n(x_i(t),y_i(t),t).
\]

A uniform random deviate \(U_i(t)\sim U(0,1)\) was sampled and division occurred if

\[
U_i(t)<g_i(t).
\]

This stochastic agent-level parameter should not be interpreted as identical to a population-level logistic growth rate subsequently fitted to simulation output.

## Migration

Cells underwent an unbiased random walk. Passage-dependent motility was described by

\[
m(p)=
\begin{cases}
1,&p<20,\\
(30-p)/10,&20\le p<30,\\
0,&p\ge30.
\end{cases}
\]

Local crowding further attenuated migration. Let \(\eta_i(t)\) be the number of neighboring fibroblasts within 0.5 patches. The crowding factor was

\[
q(\eta)=
\begin{cases}
1,&\eta=0,\\
0.6,&1\le\eta\le2,\\
0.3,&3\le\eta\le4,\\
0.1,&\eta>4.
\end{cases}
\]

The attempted hourly displacement was therefore

\[
d_i(t)=M\,m(p_i(t))\,q(\eta_i(t)),
\]

where \(M\) is the baseline migration parameter. Under the current spatial calibration of 1 patch = 20 µm, the corresponding nominal physical displacement is

\[
d_i^{\mu m}(t)=20M\,m(p_i(t))\,q(\eta_i(t)).
\]

Movement direction was randomized each hour. A move was rejected if the final position placed the cell within 0.1 patches of another fibroblast. Coordinates outside the model domain were clamped to the nearest boundary; boundaries were therefore bounded rather than reflective.

## Initial population and treatment state

The Interface variable `initial-cell-density` is currently interpreted operationally as the absolute number of fibroblast agents created at setup. All initial cells are assigned the selected `initial-passage`, set to active, placed at random coordinates, and assigned the treatment-specific baseline proliferation parameter.

## Emergent population growth

No explicit carrying-capacity parameter is imposed in the ABM. Consequently, a carrying capacity estimated by fitting a logistic model to the simulated population trajectory is an emergent summary of the combined effects of proliferation, nutrient depletion, cell-cell interactions, space, migration, and senescence. The same principle applies to a fitted population-level logistic growth-rate parameter.

## Important modeling assumption concerning FBS

FBS currently influences proliferation twice: directly as the multiplicative factor \(FBS/10\) and indirectly by setting the initial nutrient field to \(FBS/10\). At initialization, this leads to an approximately quadratic FBS dependence in the proliferation propensity. This formulation can be retained if FBS is intentionally used to represent both direct serum-dependent mitogenic stimulation and resource abundance. Otherwise, one of the two FBS dependencies should be removed in a future model revision.
