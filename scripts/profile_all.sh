#!/bin/bash
#SBATCH --job-name=profile_npn
#SBATCH --array=0-54
#SBATCH --output=out/job_%A_%a.out
#SBATCH --error=out/job_%A_%a.err
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=60

NUM_BITS=(4 6 8 10 12 14 16 18 20 22 24)
METHODS=("brute_force_tt" "flip_swap_tt" "sifting_tt" "flip_swap_lexsat" "sifting_lexsat")

# Calculate indices for this task
INDEX_NUM_BIT=$((SLURM_ARRAY_TASK_ID / ${#METHODS[@]}))
INDEX_METHOD=$((SLURM_ARRAY_TASK_ID % ${#METHODS[@]}))

# Get the parameters for this task
NUM_BIT=${NUM_BITS[$INDEX_NUM_BIT]}
METHOD=${METHODS[$INDEX_METHOD]}

# Run the profiling script with the selected parameters
python scripts/profile.py --method $METHOD --num-bit $NUM_BIT
