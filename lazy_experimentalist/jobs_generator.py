from itertools import product
from typing import Generator

from lazy_experimentalist.job import Job


def generate_jobs(
    base_cmd: str,
    output_path_pname: str,
    output_path: str,
    params: dict
) -> Generator[Job, None, None]:
  if not all(isinstance(val, list) or isinstance(val, tuple) for
             val in params.values()):
    raise ValueError(
      'Params should be a dictionary of lists or tuple of parameter '
      'possilibities.'
    )
  for combination in product(*params.values()):
    combination_params = dict(zip(params.keys(), combination))
    yield Job(base_cmd, output_path_pname, output_path, combination_params)
