import os
import pathlib
import sys

try:
    from aiida import load_profile, orm
    from aiida.orm import load_code, load_computer
    from aiida_shell.data.code import ShellCode
except ImportError:
    print("AiiDA is not installed. Please install AiiDA to use this module.")
    sys.exit(1)

from common import AIIDA_PROFILE

HOME = pathlib.Path.home()

def setup_profile():
    """Setup AiiDA profile."""
    AIIDA_PATH = pathlib.Path(os.getenv('AIIDA_PATH', HOME / '.aiida_aitw'))
    try:
        profile = load_profile(AIIDA_PROFILE)
    except:
        from aiida.manage.configuration import create_profile
        from aiida.manage.configuration.config import Config

        filepath = AIIDA_PATH / 'config.json'
        config = Config.from_file(filepath=filepath)
        profile = create_profile(
            config=config,
            name=AIIDA_PROFILE,
            email='aitw@localhost',
            storage_backend='core.sqlite_dos',
            storage_config={}
        )
        config.set_option('runner.poll.interval', 1, scope=profile.name)
        config.set_option('caching.default_enabled', True, scope=profile.name)
        config.set_default_profile(profile.name, overwrite=True)
        config.store()

        profile = load_profile(profile.name, allow_switch=True)

    return profile

def setup_computer():
    """Setup codes for the workflow."""
    try:
        computer = load_computer('localhost_EESSI')
    except:
        computer = orm.Computer(
            hostname='localhost',
            transport_type='core.local',
            scheduler_type='core.direct',
            label='localhost_EESSI',
        )
        computer.set_prepend_text('\n'.join([
            'module --force purge',
            'module unuse $MODULEPATH',
            'source /cvmfs/software.eessi.io/versions/2023.06/init/bash',
            'export OMP_NUM_THREADS=1',
            'export OMPI_MCA_osc=^ucx',
            'export OMPI_MCA_btl=^openib,ofi',
            'export OMPI_MCA_pml=^ucx',
            'export OMPI_MCA_mtl=^ofi',
            'export OMPI_MCA_btl_tcp_if_exclude=docker0,127.0.0.0/8',
        ]))
        computer.set_default_mpiprocs_per_machine(1)
        computer.set_mpirun_command('mpirun -np {tot_num_mpiprocs}'.split())
        computer.set_use_double_quotes(True)
        computer.set_shebang('#!/bin/bash')
        computer.set_workdir((HOME / '.aiida123').as_posix())
        computer.store()
        computer.configure()
    
    return computer

def setup_codes(code_infos: dict):
    computer = setup_computer()
    computer_label = computer.label

    codes = []
    for code_label, code_info in code_infos.items():
        try:
            code = load_code(f'{code_label}@{computer_label}')
        except:
            code = ShellCode(
                computer=computer,
                filepath_executable=code_info['filepath_executable']
            )
            code.label = code_label
            code.prepend_text = '\n'.join([f'module load {mod}' for mod in code_info['req_mods']])
        
            code.store()
        # print(f"Using code: {code}")
        codes.append(code)

    return codes