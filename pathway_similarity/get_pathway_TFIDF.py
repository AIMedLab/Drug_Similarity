import pickle
import numpy as np
import pandas as pd

def IDF(input_dict, drug_size, feature_size):
    input_metric = np.zeros((drug_size, feature_size)) 
    index = 0
    for key in input_dict:
        input_metric[index] = input_dict[key]
        index += 1
    big_metric = np.transpose(input_metric)
    df = big_metric.sum(1)
    # print(df)
    idf = np.log((drug_size + 1) / (df + 1))
    # print("idf:", "max:", np.max(idf), "min:", np.min(idf))
    return np.transpose(idf)  

    

def get_feature_matrix():
    with open("./did2sm.pickle", 'rb') as rf:
        drug2sm = pickle.load(rf)
    drug_size = len(drug2sm)
    #get all the drugs
    all_drug_list = list(drug2sm.keys())
    #get all pathways 
    all_pathway_list = list(set(sum(drug2sm.values(),[])))

    matrix_size = len(all_pathway_list)
    drug_pathway_matrix_dict = {}
    for drug in drug2sm:
        if drug not in drug_pathway_matrix_dict:
            drug_pathway_matrix_dict[drug] = np.zeros(matrix_size)
        for pathway in drug2sm[drug]:
            drug_pathway_matrix_dict[drug][all_pathway_list.index(pathway)] = 1

    return drug_pathway_matrix_dict, drug_size, matrix_size, all_pathway_list


if __name__ == '__main__':

    drug_pathway_matrix_dict, drug_size, matrix_size, all_pathway_list = get_feature_matrix()
    pathway_idf = IDF(drug_pathway_matrix_dict, drug_size, matrix_size)
    # print("drug size:", drug_size, "  matrix_size:", matrix_size)


    # one-hot coding ==> tfidf matrix
    for key in drug_pathway_matrix_dict.keys():
        tf = 1/np.sum(drug_pathway_matrix_dict[key]==1)
        drug_pathway_matrix_dict[key] *= (pathway_idf * tf)
    
    with open("./drug_pathway_tfidf.pickle", "wb") as wf:
       pickle.dump(drug_pathway_matrix_dict, wf)



