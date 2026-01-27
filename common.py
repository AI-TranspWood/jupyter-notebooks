STYLE = {'description_width': '150px', 'width': '400px'}
AIIDA_PROFILE = 'AITW_aiida'
WORKCHAIN_DEFAULTS = {
    'num_steps': 5000,
    'smiles_string': 'CC(=C)C(=O)OC1C[C@H]2CC[C@]1(C)C2(C)C',
    'reference_temperature': 343,
    'deform_velocities': '0.005, 0.002, 0.05, 0.02, 0.01, 0.1, 0.2',
    'num_steps_minimization': 100,
    'num_steps_equilibration': 5000,
    'num_steps_min': 100,
    'num_steps_eq': 5000,
    'force_field': 'gaff',
    'nmols': 1000,
    'time_step': 0.001,
    'averaging_start_time': 1,
}
