import os
import pathlib

home = pathlib.Path.home()

EESSI_CPU_FAMILY = os.getenv('EESSI_CPU_FAMILY')
EESSI_SOFTWARE_SUBDIR = os.getenv('EESSI_SOFTWARE_SUBDIR')
EESSI_CVMFS_REPO = os.getenv('EESSI_CVMFS_REPO')
EESSI_OS_TYPE = os.getenv('EESSI_OS_TYPE')
EESSI_SOFTWARE_PATH = os.getenv('EESSI_SOFTWARE_PATH')
EESSI_VERSION = os.getenv('EESSI_VERSION')

if EESSI_VERSION:
    EESSI_EXTEND_SOFTWARE_PATH = (
        home / 'eessi' / 'versions' / EESSI_VERSION /
        'software' / EESSI_OS_TYPE / EESSI_SOFTWARE_SUBDIR / 'software'
    ).as_posix()

STYLE = {'description_width': '150px', 'width': '600px'}
AIIDA_PROFILE = 'AITW_aiida'

WOOD_MS_DEFAULTS = {
    'wood_type': 'birch',
    'json_file': '../example-inputs/example_birch.json',
    'output_dir': '../results/wood_ms_results',
    'output_formats': 'png,tiff',
    'verbose': 1,
}

STIFFNESS_DEFAULTS = {
    'input_file': '../example-inputs/SurrogateStiffness.json',
    'output_file': '../results/stiffness_results.json',
    'lower_bound_percentage': 0.05,
    'upper_bound_percentage': 0.95,
}

VISCOSITY_WORKCHAIN_DEFAULTS = {
    'num_steps': 500,
    'smiles_string': 'CC(=C)C(=O)OC1C[C@H]2CC[C@]1(C)C2(C)C',
    'reference_temperature': 343,
    'deform_velocities': '0.005, 0.002, 0.05, 0.02, 0.01, 0.1, 0.2',
    'num_steps_minimization': 100,
    'num_steps_equilibration': 500,
    'num_steps_min': 100,
    'num_steps_eq': 500,
    'force_field': 'gaff2',
    'nmols': 1000,
    'time_step': 0.001,
    'averaging_start_time': 0.1,
}

# Mapp function imput parameters to created code names
VISCOSITY_CODE_MAP = {
    'acpype_code': 'acpype',
    'obabel_code': 'obabel',
    'veloxchem_code': 'veloxchem',
    'gmx_code': 'gromacs',
    'gmx_code_local': 'gromacs',
}

VISCOSITY_CODES = {
    'acpype': {
        # 'filepath_executable': '$HOME/eessi/versions/2023.06/software/linux/x86_64/intel/haswell/software/acpype/2023.10.27-foss-2023a/bin/acpype',
        'filepath_executable': f'{EESSI_SOFTWARE_PATH}/software/acpype/2023.10.27-foss-2023a/bin/acpype',
        'req_mods': ['acpype/2023.10.27-foss-2023a'],
    },
    'obabel': {
        # 'filepath_executable': '$HOME/eessi/versions/2023.06/software/linux/x86_64/intel/haswell/software/OpenBabel/3.1.1-gompi-2023a/bin/obabel',
        'filepath_executable': f'{EESSI_SOFTWARE_PATH}/software/OpenBabel/3.1.1-gompi-2023a/bin/obabel',
        'req_mods': ['OpenBabel/3.1.1-gompi-2023a'],
    },
    'veloxchem': {
        # 'filepath_executable': '/cvmfs/software.eessi.io/versions/2023.06/software/linux/x86_64/intel/haswell/software/Python/3.11.3-GCCcore-12.3.0/bin/python',
        'filepath_executable': f'{EESSI_SOFTWARE_PATH}/software/Python/3.11.3-GCCcore-12.3.0/bin/python',
        'req_mods': ['VeloxChem/1.0-rc4-foss-2023a'],
    },
    'gromacs': {
        # 'filepath_executable': '/cvmfs/software.eessi.io/versions/2023.06/software/linux/x86_64/intel/haswell/software/GROMACS/2024.4-foss-2023b/bin/gmx_mpi',
        'filepath_executable': f'{EESSI_SOFTWARE_PATH}/software/GROMACS/2024.4-foss-2023b/bin/gmx_mpi',
        'req_mods': ['GROMACS/2024.4-foss-2023b'],
    },
}
