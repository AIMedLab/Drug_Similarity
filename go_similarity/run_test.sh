#!/bin/bash
#SBATCH --account=xxxx
#SBATCH --job-name=goterm_similarity_perdrug
#SBATCH --time=50:00:00
#SBATCH --nodes=1 --ntasks-per-node=40
#SBATCH --output=goterm_test.out

echo "Job started..."
python Go_similarity.py $1 >> "result$1.txt"
echo "Job finished"
