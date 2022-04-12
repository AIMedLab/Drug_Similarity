import math
import pickle
import argparse
import itertools
import time
import multiprocessing 
from multiprocessing import Pool
import os 
import numpy as np
import functools
from pygosemsim import term_set
from pygosemsim import graph
from pygosemsim import annotation
from pygosemsim import similarity

parser = argparse.ArgumentParser(description='Go Similarity')
parser.add_argument('idx', default = 0, type = int)

args = parser.parse_args()

df1 = pickle.load(open('./did2pid.pickle', 'rb'))
drug_list = []
for did in df1.keys():
    drug_list.append(did)
# drug_list = ["DB01076","DB00227","DB08860","DB00175","DB01098","DB00641"]
n = len(drug_list)
# print(n)

def get_similarity_pair(drug1, drug2):
    G = graph.from_resource("go-basic")
    annot = annotation.from_resource("goa_human")
    sim = []
    pid_list1 = df1.get(drug1)
    pid_list2 = df1.get(drug2)
    for pid1 in pid_list1:
        for pid2 in pid_list2:
            trpv1 = [go_id for go_id, type in annot[pid1]["annotation"].items() if type == 'P']
            trpa1 = [go_id for go_id, type in annot[pid2]["annotation"].items() if type == 'P']
            sf = functools.partial(term_set.sim_func,G, similarity.wang)
            sim.append(term_set.sim_bma(trpv1, trpa1, sf))
            sim_list = list(filter(None, sim)) 
    # print(sim_list)
    sim_score = np.nanmean(sim_list)
    sim_score = round(sim_score,3)

    return sim_score

def process(idx):
    with Pool(processes=40) as pool:
        pair = list(itertools.product(drug_list, repeat=2))
        result = []
        result.append(pool.starmap(get_similarity_pair, pair[idx:idx+n]))
        pool.close()
        pool.join()
    return result



def main():
    start = time.time()
    idx = args.idx
    result = process(idx)
    end = time.time() 

    return result

if __name__ == "__main__":
    print(main())