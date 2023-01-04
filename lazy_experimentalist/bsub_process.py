from typing import Any
import subprocess as sp
import sys
import time
from typing import Optional


class BsubProcess:
    def __init__(self, cmd: str):
        p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        p.wait()
        res = p.stdout.read().strip().decode("utf-8", "replace")  # type: ignore
        err = p.stderr.read().strip().decode("utf-8", "replace")  # type: ignore
        if p.returncode == 255:
            raise NotImplementedError("LSF bsub system not found.")
        elif p.returncode != 0:
            if res:
                sys.stderr.write(res)
            if err:
                sys.stderr.write(err)
            raise RuntimeError(cmd + "[" + str(p.returncode) + "]")
        self.job_id = res.split("<", 1)[1].split(">", 1)[0]

    def poll(self) -> Optional[int]:
        job_info = (
            sp.check_output(["bjobs", "-w", self.job_id])
            .decode()
            .strip()
            .split("\n")[1]
        )
        print("Job info {}".format(job_info))
        if job_info.split(None, 7)[2] in ["RUN", "PEND"]:
            return None
        if job_info.split(None, 7)[2] == "DONE":
            return 0
        elif job_info.split(None, 7)[2] == "EXIT":
            verbose_info = (
                sp.check_output(["bjobs", "-l", self.job_id]).decode().strip()
            )
            exit_str = "Exited with exit code"
            error_code_start_idx = verbose_info.find(exit_str) + len(exit_str) + 1
            error_code_end_idx = error_code_start_idx
            while verbose_info[error_code_end_idx].isdigit():
                error_code_end_idx += 1
            return int(verbose_info[error_code_start_idx:error_code_end_idx])
        return None

    def wait(self, _: Any) -> int:
        while True:
            return_code = self.poll()
            if return_code is None:
                time.sleep(30)
            else:
                return return_code

    def terminate(self):
        sp.run(["bkill", self.job_id])
