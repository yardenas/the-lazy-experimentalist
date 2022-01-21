import signal
import subprocess as sp
import sys
import time
from contextlib import contextmanager
from typing import Union


class BsubProcess:
  def __init__(self, cmd: str):
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    res = p.stdout.read().strip().decode("utf-8", "replace")
    err = p.stderr.read().strip().decode("utf-8", "replace")
    if p.returncode == 255:
      raise NotImplementedError("LSF bsub system not found.")
    elif p.returncode != 0:
      if res:
        sys.stderr.write(res)
      if err:
        sys.stderr.write(err)
      raise RuntimeError(cmd + "[" + str(p.returncode) + "]")
    self.job_id = res.split("<", 1)[1].split(">", 1)[0]

  def poll(self) -> Union[int, None]:
    job_info = sp.check_output(["bjobs", "-w", self.job_id]).decode().strip()
    if job_info.split(None, 7)[2] == 'RUN':
      return None
    if job_info.split(None, 7)[2] == 'DONE':
      return 0
    elif job_info.split(None, 7)[2] == 'EXIT':
      verbose_info = (sp.check_output(["bjobs", "-l", self.job_id])
                      .decode()
                      .rstrip())
      exit_str = 'Exited with exit code'
      error_code_start_idx = verbose_info.find(exit_str) + len(exit_str) + 1
      error_code_end_idx = error_code_start_idx
      while verbose_info[error_code_end_idx].isdigit():
        error_code_end_idx += 1
      return int(verbose_info[error_code_start_idx:error_code_end_idx])

  def wait(self, timeout=None) -> int:
    with _timeout(timeout or 0):
      sleep_time = 60
      while True:
        return_code = self.poll()
        if return_code is None:
          time.sleep(sleep_time)
        else:
          return return_code

  def terminate(self):
    sp.run(["bkill", self.job_id])


@contextmanager
def _timeout(timeout):
  def handle_timeout(*_):
    raise TimeoutError

  signal.signal(signal.SIGALRM, handle_timeout)
  signal.alarm(timeout)
  try:
    yield
  finally:
    signal.signal(signal.SIGALRM, signal.SIG_IGN)