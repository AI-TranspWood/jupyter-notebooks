# AITW Jupyter Notebooks

## WoodMicrostructureGeneration

Provides a Jupyter-based interface to the `wood_ms generate` command, to generate wood microstructures.

Requires one of:

- [AITW_wood_microstructure](https://github.com/AI-TranspWood/AITW_microstructures) Python package installed or the
- [`AITW-microstructures` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW-microstructures/) loaded

## SurrogateStiffness

Provides a Jupyter-based interface to the `aitw-stiffness` command, to compute wood fiber's stiffness through a surrogate model.

Requires one of:

- [AITW_stiffness_surrogate](https://github.com/AI-TranspWood/biocomposite-surrogate) package installed or the
- [`AITW-stiffness` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW-stiffness/) loaded

## MolecularViscosity

Provides a Jupyter-based interface to the `aitw-viscosity` command, to compute the viscosity of a monomer using GROMACS.

Also provides utilities to:

- Setup an AiiDA profile with local EESSI installation of computer and codes.
- Run the `MonomerViscosity` workflow using AiiDA.
- Plot the results of the `MonomerViscosity` workflow.

Requires one of:

- [AITW-aiida-viscosity](https://github.com/AI-TranspWood/Molecular-liquid-shear-viscosity) package installed or the
- [`AITW-viscosity` EESSI module](https://www.eessi.io/docs/available_software/detail/AITW-viscosity/) loaded
