# ODD protocol summary

This document presents the model using the Overview, Design concepts, and Details (ODD) structure commonly used for agent-based models.

## 1. Overview

### 1.1 Purpose
The model is designed to study how fibroblast proliferation and migration emerge from treatment-specific proliferative capacity, serum availability, replicative passage, stochastic cell-cycle timing, local crowding, paracrine support, nutrient depletion, and spatial constraints.

### 1.2 Entities, state variables, and scales
The principal entities are fibroblast agents and environmental patches. Fibroblasts possess spatial coordinates, passage number, activity state, treatment-specific baseline proliferation parameter, elapsed time since division, and an individual division threshold. Patches contain a scalar nutrient variable.

One simulation tick represents 1 h. The working spatial calibration is 1 patch = 20 µm for migration-speed interpretation.

### 1.3 Process overview and scheduling
At each tick, each fibroblast:

1. increments its time-since-division;
2. if active, chooses a random migration direction;
3. computes passage- and crowding-modified displacement and attempts movement;
4. evaluates contact inhibition, paracrine support, and senescence;
5. reads and consumes local nutrients;
6. if its division threshold has elapsed, performs a Bernoulli division trial;
7. if division succeeds, increments passage, resets its cell-cycle clock, resamples its threshold, and creates a daughter cell with an independently sampled threshold.

After all fibroblasts have been processed, the global NetLogo tick advances by one.

## 2. Design concepts

### 2.1 Basic principles
Population-level growth is not prescribed by an explicit logistic equation. Instead, macroscopic saturation emerges from local rules governing proliferation, nutrient depletion, cell-cell interactions, senescence, migration, and spatial exclusion.

### 2.2 Emergence
Population size, apparent carrying capacity, and an apparent population-level growth rate are emergent outcomes. Logistic parameters fitted after simulation are summary descriptors rather than direct ABM inputs.

### 2.3 Adaptation
Cells do not optimize behavior. Their effective proliferation and migration change deterministically or stochastically in response to local state variables and passage.

### 2.4 Objectives
Agents have no explicit objective function.

### 2.5 Learning
No learning is implemented.

### 2.6 Prediction
Agents do not forecast future states.

### 2.7 Sensing
Cells sense local neighbor counts within specified radii and the nutrient level of their current patch.

### 2.8 Interaction
Interactions are implicit through local neighbor counts, paracrine support, contact inhibition, crowding-dependent migration, and collision avoidance.

### 2.9 Stochasticity
Stochastic processes include initial spatial placement, initial cell-cycle phase, normally distributed division thresholds, random migration direction, and hourly Bernoulli division events.

### 2.10 Collectives
No explicit higher-order collective entity is represented. Population-level patterns arise from individual-cell rules.

### 2.11 Observation
Typical outputs include total cell number as a function of time, passage-related summary statistics, and CSV parameter-screen outputs. Population trajectories can subsequently be fitted with logistic models in Python.

## 3. Details

### 3.1 Initialization
At setup, all patches receive nutrient level `FBS / 10`. The number of fibroblast agents is set by `initial-cell-density`, currently interpreted as an absolute count. Cells are positioned randomly and assigned the chosen treatment, initial passage, active state, treatment-specific baseline proliferation rate, randomized initial cell-cycle phase, and a stochastic division threshold.

### 3.2 Input data
The current NetLogo implementation does not read external biological data files at runtime. Treatment-specific baseline proliferation parameters are embedded directly in the model source. Parameter-screen outputs are written as CSV files for downstream analysis.

### 3.3 Submodels

#### Senescence
\[
s(p)=1\;(p<10),\quad s(p)=(30-p)/20\;(10\le p<30),\quad s(p)=0\;(p\ge30).
\]

#### Passage-dependent migration
\[
m(p)=1\;(p<20),\quad m(p)=(30-p)/10\;(20\le p<30),\quad m(p)=0\;(p\ge30).
\]

#### Contact inhibition
Proliferation is set to zero when more than four other cells occur within 0.3 patches.

#### Paracrine support
The multiplier is 0.1 with no neighbors within 1 patch, 0.5 with one neighbor, and 1 with two or more neighbors.

#### Crowding-dependent migration
The migration multiplier is 1 for zero neighbors within 0.5 patches, 0.6 for one to two neighbors, 0.3 for three to four neighbors, and 0.1 for more than four neighbors.

#### Nutrient consumption
Each active cell removes 0.001 nutrient units from its current patch per hour. Nutrients are bounded below at zero.

#### Division
Once a cell reaches its stochastic threshold, it attempts division hourly with probability
\[
g_i(t)=r_i(FBS/10)s(p_i)C_iP_i n(x_i,y_i,t).
\]

#### Movement
Attempted hourly displacement is
\[
d_i(t)=M m(p_i)q(\eta_i).
\]
Movement direction is random; moves that create a neighbor closer than 0.1 patches are reverted. Coordinates are clamped at the world boundary.
