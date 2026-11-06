# AITW Jupyter Notebooks

## Clearwood Stiffness

Provides a Jupyter Notebook interface to the `Clearwood_stiffness_model` Julia package that contains a neural network model for clearwood unit cell analysis.

Requires one of:
- [Clearwood_stiffness_model](https://github.com/AI-TranspWood/Clearwood_share) julia package installed or the
- [`AITW-Clearwood_stiffness_model` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW-Clearwood_stiffness_model/) loaded

## Darcy Infiltration

Provides a Jupyter Notebook interface to the `aitw-darcy` command for computing the saturation time of an infiltration process in a wood microstructure.

Requires one of:
- [AITW-darcy_infiltration](https://github.com/AI-TranspWood/AITW-Darcy-Infiltration-Model) python package installed or the
- [`AITW-darcy_infiltration` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW-darcy_infiltration/) loaded

## MolecularViscosity

Provides a Jupyter-based interface to the `aitw-viscosity` command, to compute the viscosity of a monomer using GROMACS.

Also provides utilities to:

- Setup an AiiDA profile with local EESSI installation of computer and codes.
- Run the `MonomerViscosity` workflow using AiiDA.
- Plot the results of the `MonomerViscosity` workflow.

Requires one of:

- [AITW-aiida-viscosity](https://github.com/AI-TranspWood/Molecular-liquid-shear-viscosity) python package installed or the
- [`AITW-viscosity` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW-viscosity/) loaded

## Permeability Workchain

Provides a Jupyter Notebook interface to the `aitw-permeability` commands for computing the wood permeability using a Lattice-Boltzmann method (LBM) from [OpenLB](https://www.openlb.net/) implemented as an AiiDA workchain.

Also provides utilities to:

- Setup an AiiDA profile with local EESSI installation of computer and codes.
- Run the `WoodPermeabilityWorkChain` workflow using AiiDA.
- Plot the results of the `WoodPermeabilityWorkChain` workflow.

Requires one of:

- [aiida-wood-permeability](https://github.com/AI-TranspWood/aiida_wood_permeability) python package installed or the
- [`AITW-aiida-wood-permeability` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW-aiida-wood-permeability/) loaded


## Surrogate Infiltration

Provides a Jupyter Notebook interface to the `aitw-infiltration-surrogate` command for computing the infiltration process time of a wood microstructure based on a surrogate model.

Requires one of:

- [AITW_infiltration_surrogate](https://github.com/AI-TranspWood/AITW-infiltration-surrogate) python package installed or the
- [`AITW_infiltration_surrogate` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW_infiltration_surrogate/) loaded

## Surrogate Stiffness

Provides a Jupyter Notebook interface to the `aitw-stiffness` and `aitw-material-optimization` commands for computing the stiffness of wood fibers using a TensorFlow Probability based surrogate model or use a Bayesian method to optimize the cell wall composition of a wood fiber for a target stiffness.

Requires one of:

- [AITW_stiffness_surrogate](https://github.com/AI-TranspWood/biocomposite-surrogate) python package installed or the
- [AITW_material_optimization](https://github.com/AI-TranspWood/biocomposite-surrogate) python package installed or the

or

- [`AITW-stiffness` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW-stiffness/) loaded
- [`AITW-AITW-material_optimization` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW-material_optimization/) loaded


## Surrogate Viscosity

Provides a Jupyter Notebook interface to the `aitw-viscosity-surrogate` command for computing the viscosity of a compound based on its SMILES representation using molecular descriptors and machine learning models.

Requires one of:

- [AITW_viscosity_surrogate](https://github.com/AI-TranspWood/viscosity-surrogate) python package installed or the
- [`AITW_viscosity_surrogate` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW_viscosity_surrogate/) loaded

## WoodMicrostructureGeneration

Provides a Jupyter-based interface to the `wood_ms generate` command, to generate wood microstructures both analytically and with a surrogate model. Also provides utilities to:

- Apply a porosity and binarization filter to the structures to prepare them for an LBM simulation.
- Train a new set of surrogate model weights

Requires one of:

- [AITW_wood_microstructure](https://github.com/AI-TranspWood/AITW_microstructures) Python package installed or the
- [`AITW-microstructures` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW-microstructures/) loaded

## Wood Stiffness Homogenization

Provides a Jupyter Notebook interface to the `aitw-wood-stiffness-homogenization` command for computing multiscale stiffness of native, polymer-infiltrated, and delignified + infiltrated wood.

Requires one of:

- [wood_stiffness_homogenization](https://github.com/AI-TranspWood/Wood_Stiffness_Homogenization) python package installed or the
- [`AITW-wood_stiffness_homogenization` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW-wood_stiffness_homogenization/) loaded
