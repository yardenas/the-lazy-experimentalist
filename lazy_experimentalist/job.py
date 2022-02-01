import os.path as path
from dataclasses import dataclass
from subprocess import TimeoutExpired
from typing import Optional, Callable, Any


def check_processs(fun: Callable) -> Callable:
  def wrap(job, *args, **kwargs):
    if job.process is not None:
      fun(job, *args, **kwargs)
    else:
      print("Job: {} was not launched yet.".format(job))

  return wrap


@dataclass
class Job:
  base_cmd: str
  output_path_pname: str
  output_path: str
  params: dict
  process_fn: Callable[[str], Any]
  process: Optional[Any] = None

  def launch(self):
    print("Launching {}!".format(self.__repr__()))
    params_name = ''.join('_{}-{}'.format(key, val)
                          for key, val in self.params.items())
    params_name = params_name[1:]
    output_path = str(path.join(self.output_path, params_name))
    cmd = (self.base_cmd +
           ' --{} {} '.format(self.output_path_pname, output_path) +
           ''.join('--{} {} '.format(key, value) for key, value in
                   self.params.items()))
    cmd = cmd[:-1]
    self.process = self.process_fn(cmd)
    print("Launched {}".format(self.__repr__()))

  @check_processs
  def poll(self):
    return self.process.poll()

  @check_processs
  def close(self, wait: float):
    try:
      rc = self.process.wait(wait)
      print("Closed Job: {} successfuly. Return code is: {}"
            .format(self.__repr__(), rc))
    except TimeoutExpired:
      print("Timed out while waiting for job: {}. Terminating it..."
            .format(self.__repr__()))
      self.process.terminate()

  def __hash__(self):
    return hash(tuple(sorted(self.params)))
