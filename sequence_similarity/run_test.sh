#!/bin/bash
#SBATCH --account=xxxx
#SBATCH --job-name=sequence_similarity_perdrug
#SBATCH --time=50:00:00
#SBATCH --nodes=1 --ntasks-per-node=40
#SBATCH --output=sequence_test.out

echo "Job started..."
python seq_similarity.py $1 >> "result$1.txt"
echo "Job finished"
