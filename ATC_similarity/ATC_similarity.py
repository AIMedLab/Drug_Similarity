import pickle
import numpy as np
import pandas as pd
import math
import itertools
import os 
import functools
import multiprocessing 
from multiprocessing import Pool

atc = pickle.load(open('./pickles/did2atc.pickle', 'rb'))
drug_list = []
for did in atc.keys():
    drug_list.append(did)

n = len(drug_list)

def atc_classification(atc_id):
    if not isinstance(atc_id, str):
        raise ValueError("ATC code must be a string.")

    atc_id = list(atc_id.upper())

    lv1_code = atc_id[0]
    lv2_code = ''.join(atc_id[0:3])
    lv3_code = ''.join(atc_id[0:4])
    lv4_code = ''.join(atc_id[0:5])
    # lv5_code = None
    # if len(atc_id) == 6:
    lv5_code = ''.join(atc_id)
    codes = [lv1_code, lv2_code, lv3_code, lv4_code, lv5_code]
    return codes

def get_similarity(drug1, drug2):
    atc_list1 = atc.get(drug1)
    atc_list2 = atc.get(drug2)
    code_list1 = []
    for atc1 in atc_list1:
        code_list1.append(atc_classification(atc1))
    out1 = sum(code_list1,[])
    drug1_lv1 = [code for code in out1 if len(code)==1]
    drug1_lv2 = [code for code in out1 if len(code)==3]
    drug1_lv3 = [code for code in out1 if len(code)==4]
    drug1_lv4 = [code for code in out1 if len(code)==5]
    drug1_lv5 = [code for code in out1 if len(code)==7]
    code_list2 = []
    for atc2 in atc_list2:
        code_list2.append(atc_classification(atc2))
    out2 = sum(code_list2,[])
    drug2_lv1 = [code for code in out2 if len(code)==1]
    drug2_lv2 = [code for code in out2 if len(code)==3]
    drug2_lv3 = [code for code in out2 if len(code)==4]
    drug2_lv4 = [code for code in out2 if len(code)==5]
    drug2_lv5 = [code for code in out2 if len(code)==7]

    sim1 = len(list(set(drug1_lv1).intersection(set(drug2_lv1))))/len(list(set(drug1_lv1).union(set(drug2_lv1))))
    sim2 = len(list(set(drug1_lv2).intersection(set(drug2_lv2))))/len(list(set(drug1_lv2).union(set(drug2_lv2))))
    sim3 = len(list(set(drug1_lv3).intersection(set(drug2_lv3))))/len(list(set(drug1_lv3).union(set(drug2_lv3))))
    sim4 = len(list(set(drug1_lv4).intersection(set(drug2_lv4))))/len(list(set(drug1_lv4).union(set(drug2_lv4))))
    sim5 = len(list(set(drug1_lv5).intersection(set(drug2_lv5))))/len(list(set(drug1_lv5).union(set(drug2_lv5))))
    sim = (sim1, sim2, sim3, sim4, sim5)       
    sim_score = sum(sim)/5
    sim_score = round(sim_score,3)

    return sim_score

def process():
    with Pool(processes=40) as pool:
        pair = list(itertools.combinations_with_replacement(drug_list, 2))
        p = multiprocessing.Pool()
        result = list(p.starmap(get_similarity, pair))
        # print(result)
        pool.close()
        pool.join()
    return result

def get_matrix(list,len):
    Full_matrix = np.zeros((len,len))
    inds = np.triu_indices_from(Full_matrix, k = 0)
    Full_matrix[inds] = list[:]
    Full_matrix[(inds[1], inds[0])] = list[:]
    return Full_matrix


if __name__ == '__main__':
    list = process()
    matrix = get_matrix(list,n)
    # similarity_df = pd.DataFrame(matrix)
    similarity_df = pd.DataFrame(matrix, columns = drug_list, index = drug_list)
    print(similarity_df)
    similarity_df.to_csv("ATC_similarity.csv", index = False)

