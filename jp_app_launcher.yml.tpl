######################################################################
# AITW
- title: README
  description: Notebooks description
  source: ./README.md
  type: markdown
  catalog: 1. AITW
  icon: ./images/AITW_logo.svg

- title: Clearwood Stiffness
  description: Jupyter Notebook interface to the `Clearwood_stiffness_model` Julia package that contains a neural
    network model for clearwood unit cell analysis.
  source: /voila/render/notebooks/ClearwoodStiffness.ipynb
  type: url
  icon: ./images/AITW_logo.svg
  args:
      sandbox: [ 'allow-same-origin', 'allow-scripts', 'allow-downloads', 'allow-modals', 'allow-popups']
      referrerPolicy: ['no-referrer']
      createNewWindow: false
  catalog: 1. AITW

- title: Darcy Infiltration
  description: Jupyter Notebook interface to the `aitw-darcy` command for computing the saturation time of an 
    infiltration process in a wood microstructure.
  source: /voila/render/notebooks/DarcyInfiltration.ipynb
  type: url
  icon: ./images/AITW_logo.svg
  args:
      sandbox: [ 'allow-same-origin', 'allow-scripts', 'allow-downloads', 'allow-modals', 'allow-popups']
      referrerPolicy: ['no-referrer']
      createNewWindow: false
  catalog: 1. AITW

- title: Molecular Viscosity
  description: |
    Jupyter Notebook interface to the `aitw-viscosity` commands for computing molecular viscosities starting from a
    SMILES code using GROMACS.
  source: /voila/render/notebooks/MolecularViscosity.ipynb
  type: url
  icon: ./images/AITW_logo.svg
  args:
      sandbox: [ 'allow-same-origin', 'allow-scripts', 'allow-downloads', 'allow-modals', 'allow-popups']
      referrerPolicy: ['no-referrer']
      createNewWindow: false
  catalog: 1. AITW

- title: Permeability Workchain
  description: |
    Jupyter Notebook interface to the `aitw-permeability` commands for computing the wood permeability using a
      Lattice-Boltzmann method (LBM) implemented as an AiiDA workchain.
  source: /voila/render/notebooks/PermeabilityWorkchain.ipynb
  type: url
  icon: ./images/AITW_logo.svg
  args:
      sandbox: [ 'allow-same-origin', 'allow-scripts', 'allow-downloads', 'allow-modals', 'allow-popups']
      referrerPolicy: ['no-referrer']
      createNewWindow: false
  catalog: 1. AITW

- title: Surrogate Infiltration
  description: Jupyter Notebook interface to the `aitw-infiltration-surrogate` command for computing the infiltration
    process time of a wood microstructure based on a surrogate model.
  source: /voila/render/notebooks/SurrogateInfiltration.ipynb
  type: url
  icon: ./images/AITW_logo.svg
  args:
      sandbox: [ 'allow-same-origin', 'allow-scripts', 'allow-downloads', 'allow-modals', 'allow-popups']
      referrerPolicy: ['no-referrer']
      createNewWindow: false
  catalog: 1. AITW

- title: Surrogate Stiffness
  description: Jupyter Notebook interface to the `aitw-stiffness` command for computing the stiffness of wood fibers
    using a TensorFlow Probability based surrogate model
  source: /voila/render/notebooks/SurrogateStiffness.ipynb
  type: url
  icon: ./images/AITW_logo.svg
  args:
      sandbox: [ 'allow-same-origin', 'allow-scripts', 'allow-downloads', 'allow-modals', 'allow-popups']
      referrerPolicy: ['no-referrer']
      createNewWindow: false
  catalog: 1. AITW

- title: Wood Microstructures
  description: Jupyter Notebook interface to the `wood_ms` command for generating wood microstructures both with and
    without the use of a surrogate model.
  source: /voila/render/notebooks/WoodMicrostructureGeneration.ipynb
  type: url
  icon: ./images/AITW_logo.svg
  args:
      sandbox: [ 'allow-same-origin', 'allow-scripts', 'allow-downloads', 'allow-modals', 'allow-popups']
      referrerPolicy: ['no-referrer']
      createNewWindow: false
  catalog: 1. AITW

- title: Wood Stiffness Homogenization
  description: Jupyter Notebook interface to the `aitw-wood-stiffness-homogenization` command for computing multiscale 
    stiffness of native, polymer-infiltrated, and delignified + infiltrated wood
  source: /voila/render/notebooks/WoodStiffHomog.ipynb
  type: url
  icon: ./images/AITW_logo.svg
  args:
      sandbox: [ 'allow-same-origin', 'allow-scripts', 'allow-downloads', 'allow-modals', 'allow-popups']
      referrerPolicy: ['no-referrer']
      createNewWindow: false
  catalog: 1. AITW

######################################################################
# AiiDA
- title: AiiDA Explorer
  description: Launch AiiDA REST Api + an AiiDA-explorer instance to interact with it.
  source: http://localhost:$PORT/?api_url=http://127.0.0.1:${FLASK_PORT_EXT}/api/v4
  type: local-server
  icon: ./images/aiida-icon.svg
  args:
    - ./scripts/launch_aiida_explorer.sh
    - --port
    - $PORT
  catalog: 2. AiiDA

######################################################################
# Manage
- title: UPDATE
  description: Pull the latest version of the notebooks
  type: terminal
  source: 'git pull origin main'
  cwd: './'
  icon: ./images/icons8-update.svg
  args:
    reuse: true
  catalog: 3. MANAGE
# - title: Shutdown extension
#   description: Force a restart of the extension to update the Luancher and re-run the initialization scripts
#   type: terminal
#   source: 'ps -aux | grep "jupyter-lab" | grep -v grep | tr -s " " | cut -d" " -f2 | xargs kill'
#   cwd: './'
#   args:
#     reuse: true
#   catalog: 3. MANAGE
