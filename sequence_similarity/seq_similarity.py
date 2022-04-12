#!/usr/bin/env python

import numpy as np
import math
import pickle
import itertools
import time
from multiprocessing.pool import ThreadPool
import ctypes
import argparse

parser = argparse.ArgumentParser(description='Sequence Similarity')
parser.add_argument('idx', default = 0, type = int)

args = parser.parse_args()

swg = ctypes.cdll.LoadLibrary('./swg.so')
swg.GetSimilarity.restype = ctypes.c_float
swg.GetSimilarity.argtypes = (ctypes.c_char_p, ctypes.c_char_p)

df1 = pickle.load(open('./approved_drug_uid.pickle', 'rb'))
df2 = pickle.load(open('./pid2fasta.pickle', 'rb'))
# drug_list = ["DB01076","DB00227","DB08860","DB00175","DB01098","DB00641"]
drug_list = []
for did in df1.keys():
    drug_list.append(did)

n = len(drug_list)


def get_similarity(string1, string2):
    string1 = string1.encode("utf-8")
    string2 = string2.encode("utf-8")
    value12 = float(swg.GetSimilarity(string1, string2))
    value11 = float(math.sqrt(swg.GetSimilarity(string1, string1)))
    value22 = float(math.sqrt(swg.GetSimilarity(string2, string2)))
    if ((value11 * value22) == 0):
        sim_score = 0
    else:
        sim_score = value12 / (value11 * value22)

    return sim_score

def get_similarity_pair(drug1, drug2):
    sim_score = []
    pid_list1 = df1.get(drug1)
    pid_list2 = df1.get(drug2)
    # print(pid_list1)
    # print(pid_list2)
    for pid1 in pid_list1:
        for pid2 in pid_list2:
            fasta1 = df2.get(pid1)
            fasta2 = df2.get(pid2)
            sim_score.append(get_similarity(fasta1,fasta2))
    similarity = np.mean(sim_score)
    similarity = round(similarity,3)
    # print(similarity)
    return similarity

def get_matrix(list,len):
    Full_matrix = np.zeros((len,len))
    inds = np.triu_indices_from(Full_matrix, k = 0)
    Full_matrix[inds] = list[:]
    Full_matrix[(inds[1], inds[0])] = list[:]
    return Full_matrix

def gen_result(idx):
    with ThreadPool(1024) as pool:
        pair = list(itertools.product(drug_list, repeat=2))
        result = []
        result.append(pool.starmap(get_similarity_pair, pair[idx:idx+n]))
        pool.close()
        pool.join()
    return result


def main():
    idx = args.idx
    start = time.time()
    result = gen_result(idx)
    # similarity = get_matrix(matrix, n)
    # print(result)
    # print(matrix)
    end = time.time()
    # print(end-start)
    return result

if __name__ == "__main__":
    print(main())

