import os.path as path
from dataclasses import dataclass
from typing import Dict, Optional, Callable, Any


@dataclass
class Job:
    base_cmd: str
    output_path_pname: str
    output_path: str
    params: Dict[str, Any]
    process_fn: Callable[[str], Any]
    process: Optional[Any] = None

    def launch(self):
        print("Launching {}!".format(self.__repr__()))
        params_name = "".join(
            "_{}-{}".format(key, val) for key, val in self.params.items()
        )
        params_name = params_name[1:]
        output_path = str(path.join(self.output_path, params_name))
        cmd = (
            self.base_cmd
            + " --{} {} ".format(self.output_path_pname, output_path)
            + "".join(
                "--{} {} ".format(key, value) for key, value in self.params.items()
            )
        )
        cmd = cmd[:-1]
        self.process = self.process_fn(cmd)
        print("Launched {}".format(self.__repr__()))

    def poll(self):
        assert self.process
        return self.process.poll()

    def close(self):
        assert self.process
        self.process.terminate()

    def __hash__(self):
        return hash(tuple(sorted(self.params)))
