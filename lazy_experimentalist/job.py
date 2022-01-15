import os.path as path
from dataclasses import dataclass
from subprocess import Popen, TimeoutExpired
from typing import Optional


@dataclass
class Job:
  base_cmd: str
  output_path_pname: str
  output_path: str
  params: dict
  process: Optional[Popen] = None

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
    self.process = Popen(cmd, shell=True)

  def close(self, wait: float):
    if self.process is not None:
      try:
        rc = self.process.wait(wait)
        print("Closed Job: {} successfuly. Return code is: {}"
              .format(self.__repr__(), rc))
      except TimeoutExpired:
        print("Timed out while waiting for job: {}. Terminating it..."
              .format(self.__repr__()))
        self.process.terminate()
    else:
      print("Job: {} was not launched yet.".format(self.__repr__()))
