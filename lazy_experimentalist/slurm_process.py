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
            raise RuntimeError(
                "Please specify base command within wrap parameter of Slurm"
            )
        params = cmd[match.end() :]
        new_wrap = match.group(0).replace(match.group(1), match.group(1) + params)
        new_cmd = cmd[: match.start()] + new_wrap
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
        try:
            exit_code, status = (
                sp.check_output(
                    ["sacct", "-j", "5139349", "-o", "ExitCode,State", "-n", "-p"]
                )
                .decode()
                .strip('""')
                .split("\n", 1)[0]
                .split("|")[:2]
            )

        except sp.CalledProcessError as e:
            print(e)
            return None
        if status == "RUNNING":
            return None
        else:
            return int(exit_code)

    def wait(self, _) -> int:
        while True:
            return_code = self.poll()
            if return_code is None:
                time.sleep(30)
            else:
                return return_code

    def terminate(self):
        sp.run(["scancel", self.job_id])
