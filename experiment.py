import argparse
import ast
import signal
import sys
import time

from lazy_experimentalist.jobs_generator import generate_jobs


def signal_handler(sig, frame, jobs):
  for job in jobs:
    print("Closing {}".format(job))
    job.close()
  sys.exit(0)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_cmd', type=str, required=True,
                      help='The base command for the that should be run.')
  parser.add_argument('--output_path_pname', default='log_dir',
                      help='The script\'s output path parameter name')
  parser.add_argument('--base_output_path', required=True,
                      help='Where to log the script\'s output.')
  parser.add_argument('-p', '--params', type=ast.literal_eval, default=dict(),
                      help='A python-typed dictionary that maps between a '
                           'parameter name and all of it\'s wanted possible '
                           'values')
  parser.add_argument('-t', '--timeout', default=5, type=float,
                      help='Time [sec] that jobs should run, or terminated '
                           'otherwise')
  args = parser.parse_args()
  jobs = set()
  for job in generate_jobs(args.base_cmd, args.output_path_pname,
                           args.base_output_path, args.params):
    jobs.add(job)
    job.launch()
  finished_ok = set()
  failed = set()
  signal.signal(signal.SIGINT,
                lambda sig, frame: signal_handler(sig, frame, jobs))
  while jobs:
    time.sleep(60)
    for job in jobs:
      return_code = job.poll()
      # Job is still running, let it run.
      if return_code is None:
        print("Job {} is still running.".format(job))
        continue
      # Job finished ok, add to finished jobs.
      elif return_code == 0:
        finished_ok.add(job)
        jobs.remove(job)
      # Job crashed due to user error.
      elif return_code == 1:
        print("Job {} crashed!".format(job))
        failed.add(job)
        jobs.remove(job)
      # Unknown crash, re-try.
      else:
        job.launch()
  print('Done...!')
  if finished_ok:
    print('The following jobs finished successfully:', *finished_ok, sep='\n')
  if failed:
    print('The following jobs failed:', *failed, sep='\n')


if __name__ == '__main__':
  main()
