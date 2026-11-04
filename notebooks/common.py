import os
import pathlib

home = pathlib.Path.home()


STYLE = {'description_width': '150px', 'width': '600px'}
AIIDA_PROFILE = 'AITW_aiida'

RESULTS_DIR = '../results'

DARCY_OUTDIR = os.path.join(RESULTS_DIR, 'darcy')
DARCY_DEFAULTS = {
    'config_file': '../example-inputs/darcy/small.json',
    'output_dir': DARCY_OUTDIR,
}

INFILTRATION_SURROGATE_OUTDIR = os.path.join(RESULTS_DIR, 'infiltration_surrogate')
INFILTRATION_SURROGATE_TRAIN_DEFAULTS = {
    'data_file': '../example-inputs/infiltration_surrogate/dataset.csv',
    'output_dir': os.path.join(INFILTRATION_SURROGATE_OUTDIR, 'train'),
}
INFILTRATION_SURROGATE_INFERENCE_DEFAULTS = {
    'input_file': '../example-inputs/infiltration_surrogate/dataset.csv',
    'output_file': os.path.join(INFILTRATION_SURROGATE_OUTDIR, 'inference_results.csv'),
}

WOOD_MS_OUTDIR = os.path.join(RESULTS_DIR, 'wood_ms')
WOOD_MS_DEFAULTS = {
    'wood_type': 'birch',
    'config_file': '../example-inputs/wood_ms/example_birch.json',
    'output_dir': WOOD_MS_OUTDIR,
    'output_formats': 'png,tiff',
    'verbose': 1,
}
WOOD_MS_DEFAULTS_FILTER = {
    'config_file': '../example-inputs/wood_ms/fit_porosity.json',
    'output_dir': WOOD_MS_OUTDIR,
    'input_file': os.path.join(WOOD_MS_OUTDIR, 'SaveBirch_0/FinalVolume3D/FinalVolume.nrrd'),
    'verbose': 1,
}
WOOD_MS_DEFAULTS_TRAIN = {
    'output_dir': WOOD_MS_OUTDIR,
    'verbose': 1,
}

STIFFNESS_OUTDIR = os.path.join(RESULTS_DIR, 'stiffness_surrogate')
STIFFNESS_DEFAULTS = {
    'input_file': '../example-inputs/surrogate_stiff/SurrogateStiffness.json',
    'output_file': os.path.join(STIFFNESS_OUTDIR, 'stiffness_results.json'),
    'lower_bound_percentage': 0.05,
    'upper_bound_percentage': 0.95,
}
STIFFNESS_OPTIM_OUTDIR = os.path.join(RESULTS_DIR, 'stiffness_optimization')
STIFFNESS_OPTIMIZATION_DEFAULTS = {
    'input_file': '../example-inputs/surrogate_stiff/matching-material.json',
    'output_spec_file': '../example-inputs/surrogate_stiff/matching-outputs.json',
    'result_file': os.path.join(STIFFNESS_OPTIM_OUTDIR, 'stiffness_results.json'),
    'mode':'matching',
}

HOMOG_STIFFNESS_OUTDIR = os.path.join(RESULTS_DIR, 'stiff_homog')
WOOD_SITFFNESS_HOMOG_DEFAULTS = {
    'config_file': '../example-inputs/stiff_homog/birch_batch.json',
    'output': os.path.join(HOMOG_STIFFNESS_OUTDIR, 'birch_batch.csv'),
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
        'filepath_executable': f'acpype',
        'req_mods': ['EESSI/2023.06', 'acpype/2023.10.27-foss-2023a'],
    },
    'obabel': {
        # 'filepath_executable': '$HOME/eessi/versions/2023.06/software/linux/x86_64/intel/haswell/software/OpenBabel/3.1.1-gompi-2023a/bin/obabel',
        'filepath_executable': f'obabel',
        'req_mods': ['EESSI/2023.06', 'OpenBabel/3.1.1-gompi-2023a'],
    },
    'veloxchem': {
        # 'filepath_executable': '/cvmfs/software.eessi.io/versions/2023.06/software/linux/x86_64/intel/haswell/software/Python/3.11.3-GCCcore-12.3.0/bin/python',
        'filepath_executable': f'python',
        'req_mods': ['EESSI/2023.06', 'VeloxChem/1.0-rc4-foss-2023a'],
    },
    'gromacs': {
        # 'filepath_executable': '/cvmfs/software.eessi.io/versions/2023.06/software/linux/x86_64/intel/haswell/software/GROMACS/2024.4-foss-2023b/bin/gmx_mpi',
        'filepath_executable': f'gmx_mpi',
        'req_mods': ['EESSI/2023.06', 'GROMACS/2024.4-foss-2023b'],
    },
}

PERMEABILITY_WORKCHAIN_INPUTDIR = '../example-inputs/permeability_workchain'
PERMEABILITY_WORKCHAIN_DEFAULTS = {
    'wood_type': 'birch',
    'generate_params_file': os.path.join(PERMEABILITY_WORKCHAIN_INPUTDIR, 'wood_ms_birch_small.json'),
    'filter_params_file': os.path.join(PERMEABILITY_WORKCHAIN_INPUTDIR, 'fit_porosity.json'),
    'resolution': 45,
}

PERMEABILITY_CODE_MAP = {
    'wood_ms': 'wood_ms',
    'permeability_code': 'permeability_olb',
}

PERMEABILITY_CODES = {
    'wood_ms': {
        'filepath_executable': f'wood_ms',
        'req_mods': ['EESSI/2023.06', 'AITW-microstructures/1.2.0-foss-2023a'],
    },
    'permeability_olb': {
        'filepath_executable': f'PermPorousWood',
        'req_mods': ['EESSI/2023.06', 'AITW-olb_permeability/1.0.1-foss-2023b'],
    },
}