from functools import partial
from itertools import product
from subprocess import Popen
from typing import Generator, Type, Union

from lazy_experimentalist.bsub_process import BsubProcess
from lazy_experimentalist.job import Job
from lazy_experimentalist.slurm_process import SlurmProcess


def map_command_to_scheduler(
    base_cmd: str,
) -> Union[Type[BsubProcess], partial, Type[SlurmProcess]]:
    if base_cmd.startswith("bsub"):
        return BsubProcess
    elif base_cmd.startswith("sbatch"):
        return SlurmProcess
    else:
        return partial(Popen, shell=True)


def generate_jobs(
    base_cmd: str, output_path_pname: str, output_path: str, params: dict
) -> Generator[Job, None, None]:
    if not all(
        isinstance(val, list) or isinstance(val, tuple) for val in params.values()
    ):
        raise ValueError(
            "Params should be a dictionary of lists or tuple of parameter "
            "possilibities."
        )
    base_cmd = base_cmd.strip()
    process_fn: Union[
        Type[BsubProcess], partial, Type[SlurmProcess]
    ] = map_command_to_scheduler(base_cmd)
    if not params:
        yield Job(base_cmd, output_path_pname, output_path, {}, process_fn)
        return
    for combination in product(*params.values()):
        combination_params = dict(zip(params.keys(), combination))
        yield Job(
            base_cmd, output_path_pname, output_path, combination_params, process_fn
        )
