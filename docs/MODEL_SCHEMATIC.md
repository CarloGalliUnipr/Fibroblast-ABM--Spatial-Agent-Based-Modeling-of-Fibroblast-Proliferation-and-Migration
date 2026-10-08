# Model schematic

![Schematic of the fibroblast agent-based model](../assets/model_schematic.png)

## Figure description

The schematic summarizes the organization of the fibroblast agent-based model (ABM). The simulated environment is a two-dimensional NetLogo domain composed of patches, each carrying a local nutrient variable, `nutrients`. Individual fibroblasts are represented as mobile agents with continuous spatial coordinates and cell-specific state variables including replicative passage, treatment-dependent baseline growth propensity, time since division, and a stochastic division threshold.

At each hourly simulation step, cells interact with their local neighborhood through four main mechanisms. First, **paracrine support** increases the proliferation propensity of cells that have nearby neighbors within a radius of 1 patch. Second, **contact inhibition** suppresses proliferation when more than four neighboring cells are located within a short-range radius of 0.3 patches. Third, **crowding-dependent migration** reduces the attempted displacement of cells as the number of neighbors within 0.5 patches increases. Fourth, each active cell consumes nutrient from the patch on which it is located. Replicative passage additionally reduces proliferation and, at higher passage, migration.

For proliferation-eligible cell \(i\), the effective hourly growth propensity is

\[
g_i(t)=r_i\left(\frac{FBS}{10}\right)s(p_i(t))C_i(t)P_i(t)n(x_i(t),y_i(t),t),
\]

where \(r_i\) is the treatment-specific baseline growth parameter, \(s\) is the passage-dependent senescence factor, \(C_i\) is the contact-inhibition factor, \(P_i\) is the paracrine-stimulation factor, and \(n\) is the nutrient level of the occupied patch. A division trial is performed only after the cell-specific stochastic cell-cycle threshold has elapsed.

The attempted migration distance is

\[
d_i(t)=M\,m(p_i(t))\,q(\eta_i(t)),
\]

where \(M\) is the baseline migration setting, \(m(p_i)\) is the passage-dependent motility factor, and \(q(\eta_i)\) is the local crowding factor. Movement direction is random, the simulation boundary is clamped, and an attempted move is rejected when it would place a cell within 0.1 patches of another cell.

Population growth, spatial spreading, and apparent growth saturation therefore arise from the combined agent-level and local-environment rules rather than from an imposed population-level logistic equation or carrying-capacity parameter.

## Suggested manuscript caption

**Figure X. Schematic representation of the fibroblast agent-based model.** Fibroblasts are represented as individual mobile agents within a two-dimensional NetLogo domain containing a patch-level nutrient field. Each cell is characterized by spatial position, replicative passage, treatment-dependent baseline proliferation propensity, time since the previous division, and a stochastic division threshold. Proliferation is modulated by serum availability, passage-dependent senescence, short-range contact inhibition, local paracrine support, and nutrient availability. Migration is modeled as an unbiased random walk whose displacement decreases with replicative passage and local crowding. Cells consume nutrients locally and attempted moves that result in close overlap are rejected. Population-level growth and spatial organization emerge from these local rules rather than from an explicitly imposed logistic growth law.
