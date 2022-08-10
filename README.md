# the-lazy-experimentalist
Helping myself run more (remote) experiments with less (fingers) effort

# Example command

```
python /cluster/home/yardas/the-lazy-experimentalist/experiment.py --base_cmd "bsub -g /yardas -G ls_krausea -n 12  -W 24:00 -R "rusage[ngpus_excl_p=1,mem=10000]" -R "select[gpu_model0==NVIDIAGeForceRTX2080Ti]" python scripts/domain_randomization_experiment.py" --base_output_path /cluster/scratch/yardas/dbg --params "{'agent': ['maml_ppo_lagrangian', 'rl2_cpo', 'rarl_cpo']}"
```
