# the-lazy-experimentalist
Helping myself run more (remote) experiments with less (fingers) effort

# Example command

```python /cluster/home/yardas/the-lazy-experimentalist/experiment.py --base_cmd bsub -g /yardas -W 24:00 -R "rusage[ngpus_excl_p=1,mem=100000]" -R "select[gpu_model0==GeForceRTX2080Ti]" python experiments/log_barrier/meta/train_meta.py --robot Car --task Goal --total_training_steps 1000000 --seed 12345 --safety --start_lagrangian --base_output_path /cluster/scratch/yardas/lagrangian_interior/car_goal --params {"backup_lr": [0.01, 0.001, 1e-1, 0.5, 1.0], "seed": [1, 12, 123, 1234, 1235]}```
