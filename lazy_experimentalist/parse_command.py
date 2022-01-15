from typing import List


def parse_parameters(params: List[List[str]]) -> str:
  command = ''
  for param_range in params:
    command += '--{} '.format(param_range.pop())
    for param in param_range:
      command += '{} '.format(param)
  return command
