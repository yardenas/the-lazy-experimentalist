# the-lazy-experimentalist
Helping myself run more (remote) experiments with less (fingers) effort

# Example command

```
 python /cluster/home/yardas/the-lazy-experimentalist/experiment.py --base_cmd "bsub -g /yardas -W 24:00 -R "rusage[ngpus_excl_p=1,mem=100000]" -R "select[gpu_model0==GeForceRTX2080Ti]" python experiments/log_barrier/offline/demonstration_seed.py --total_training_steps 1000000  --safety" --base_output_path /cluster/scratch/yardas/offline_lagrangian/point_goal --params "{'seed': [1, 12, 123, 1234, 1235]}"
```
