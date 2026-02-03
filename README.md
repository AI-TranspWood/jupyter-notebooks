# AITW Jupyter Notebooks

## WoodMicrostructureGeneration

Provides a Jupyter based interface to the `wood_ms generate` command, allowing users to generate wood microstructures.

Requires one of:

- [AITW_wood_microstructure](https://github.com/AI-TranspWood/AITW_microstructures) package installed or the
- `AITW-microstructures` EESSI module loaded

## SurrogateStiffness

Provides a Jupyter based interface to the `aitw-stiffness` for computing wood fiber's stiffness through a surrogate model.

Requires one of:

- [AITW_stiffness_surrogate](https://github.com/AI-TranspWood/biocomposite-surrogate) package installed or the
- `AITW-stiffness` EESSI module loaded

## MolecularViscosity

Provides a Jupyter based interface to the `aitw-viscosity` command for computing the viscosity of a monomer using GROMACS.

Also provides utilities to:

- Setup and AiiDA profile with local EESSI installation of computer and codes
- Run the `MonomerViscosity` workflow using AiiDA
- Plot the results of the `MonomerViscosity` workflow

Requires one of:

- [AITW-aiida-viscosity](https://github.com/AI-TranspWood/Molecular-liquid-shear-viscosity) package installed or the
- `AITW-viscosity` EESSI module loaded
