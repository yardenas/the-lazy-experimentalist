import unittest

from lazy_experimentalist.jobs_generator import generate_jobs


class TestJobsGenerator(unittest.TestCase):
  def test_all_list(self):
    example = {'a': [1, 2, 3, 4], 'b': 1}
    with self.assertRaises(ValueError):
      yield from generate_jobs("", "", "", example)

  def test_jobs_correct(self):
    example = {'a': [1, 2],
               'd': [False]}
    jobs = [job for job in generate_jobs("", "", "", example)]
    correct_possibilities = [{'a': 1, 'd': False}, {'a': 2, 'd': False}]
    for job in jobs:
      self.assertIn(job.params, correct_possibilities)
