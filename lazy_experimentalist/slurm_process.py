import subprocess as sp
import sys
import time
from typing import Optional
import re


class SlurmProcess:
    def __init__(self, cmd: str):
        # Make sure that the new parameters are within `wrap`
        match = re.search("wrap='([^']*)'", cmd)
        if not match:
            raise RuntimeError('Please specify base command within wrap')
        params = cmd[match.end():].strip()
        new_wrap = match.group(0).replace(match.group(1), match.group(1) + params)
        new_cmd = cmd.replace(match.group(0), new_wrap)
        p = sp.Popen(new_cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        p.wait()
        res = p.stdout.read().strip().decode("utf-8", "replace")  # type: ignore
        err = p.stderr.read().strip().decode("utf-8", "replace")  # type: ignore
        if p.returncode == 255:
            raise NotImplementedError("Slurm system not found.")
        elif p.returncode != 0:
            if res:
                sys.stderr.write(res)
            if err:
                sys.stderr.write(err)
            raise RuntimeError(cmd + "[" + str(p.returncode) + "]")
        self.job_id = res.rsplit(" ", 1)[1]

    def poll(self) -> Optional[int]:
        job_info = (
            sp.check_output(["squeue", "-j", self.job_id, '-o', '\"%t\"', '-h'])
            .decode()
            .strip('\"')
        )
        print("Job info {}".format(job_info))
        if job_info == "CD":
            return 0
        elif job_info in ["F", "NF", "OOM", "SI", "SE"]:
            return 1
        elif job_info in ["TO", "DL", "PR"]:
            return 140
        return None

    def wait(self, _) -> int:
        while True:
            return_code = self.poll()
            if return_code is None:
                time.sleep(30)
            else:
                return return_code

    def terminate(self):
        sp.run(["scancel", self.job_id])
