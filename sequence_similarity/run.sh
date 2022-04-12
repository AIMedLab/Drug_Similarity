#!/bin/bash
#SBATCH --account=xxx
#SBATCH --job-name=sequence_similarity
#SBATCH --time=50:00:00
#SBATCH --nodes=1 --ntasks-per-node=40
#SBATCH --output=sequence_test.out

echo "Job started..."

for i in $(seq 0 1898);
do
   sbatch run_test.sh $(((i - 1) * 1897))
done



echo "Job finished"
