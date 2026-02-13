import os
import pathlib

AIIDA_PATH = os.getenv('AIIDA_PATH')
if AIIDA_PATH is not None:
    AIIDA_PATH = pathlib.Path(AIIDA_PATH)
else:
    AIIDA_PATH = pathlib.Path.home()
    os.environ['AIIDA_PATH'] = AIIDA_PATH.as_posix()

from contextlib import contextmanager
from functools import wraps

try:
    from aiida import load_profile, orm
    from aiida.manage.configuration import profile_context
    from aiida.orm import load_code, load_computer
    from aiida_shell.data.code import ShellCode
except ImportError:
    WITH_AIIDA = False
else:
    WITH_AIIDA = True

from common import AIIDA_PROFILE

HOME = pathlib.Path.home()

# Decorator to check that AiiDA is available
def with_aiida(func):
    """Decorator to ensure AiiDA is available before executing the function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not WITH_AIIDA:
            raise ImportError("AiiDA is not available. Please install AiiDA to use this function.")
        return func(*args, **kwargs)
    return wrapper

@contextmanager
@with_aiida
def with_aiida_profile(profile_name: str = AIIDA_PROFILE):
    """Context manager to check if AiiDA is setup with a profile available.

    Args:
        profile_name (str): Name of the AiiDA profile to switch to.
    """
    try:
        with profile_context(profile_name, allow_switch=True) as profile:
            yield profile
    except Exception as e:
        raise RuntimeError(f"Could not load AiiDA profile '{profile_name}': {e}")
    finally:
        pass

@with_aiida
def setup_profile():
    """Setup AiiDA profile."""
    try:
        profile = load_profile(AIIDA_PROFILE)
    except:
        from aiida.manage.configuration import create_profile
        from aiida.manage.configuration.config import Config

        AIIDA_PATH.mkdir(parents=True, exist_ok=True)

        filepath = AIIDA_PATH / '.aiida' / 'config.json'
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

@with_aiida
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
        computer.set_workdir((HOME / '.aiida_workdir').as_posix())
        computer.store()
        computer.configure()
    
    return computer

@with_aiida
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

@with_aiida
def get_all_codes():
    """Retrieve all codes from the AiiDA database."""
    qb = orm.QueryBuilder()
    qb.append(orm.Code)
    codes = [_[0] for _ in qb.all()]

    return codes
