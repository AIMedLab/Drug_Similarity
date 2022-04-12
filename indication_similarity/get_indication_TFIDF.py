import pickle
import numpy as np
import pandas as pd

def calculate_IDF(input_dict, drug_size, feature_size):
    input_metric = np.zeros((drug_size, feature_size)) 
    index = 0
    for key in input_dict:
        input_metric[index] = input_dict[key]
        index += 1
    big_metric = np.transpose(input_metric)
    df = big_metric.sum(1)  
    # print(df)
    idf = np.log((drug_size + 1) / (df + 1)) 
    print("idf:", "max:", np.max(idf), "min:", np.min(idf))
    return np.transpose(idf)  


def get_feature_matrix():
    did2indication = pickle.load(open('./drug2indication.pickle', 'rb')) 
    drug_size = len(did2indication)
    #get all the drugs
    all_drug_list = list(did2indication.keys())
    #get all indications
    all_indications_list = list(set(sum(did2indication.values(),[])))
    # print(all_indications_list)
    all_indications_list.sort()
    matrix_size = len(all_indications_list)
    
    drug_indications_matrix_dict = {}
    for drug in all_drug_list:
        if drug not in drug_indications_matrix_dict:
            drug_indications_matrix_dict[drug] = np.zeros(matrix_size)
        for indication in did2indication.get(drug):
            drug_indications_matrix_dict[drug][all_indications_list.index(indication)] = 1     
        

    return drug_indications_matrix_dict, drug_size, matrix_size, all_indications_list


if __name__ == '__main__':

    drug_indications_matrix_dict, drug_size, matrix_size, all_indications_list = get_feature_matrix()
    indications_idf = calculate_IDF(drug_indications_matrix_dict, drug_size, matrix_size)
    print("drug size:", drug_size, "  matrix_size:", matrix_size)
    # print(drug_indications_matrix_dict['DB11280'])

    for key in drug_indications_matrix_dict.keys():
        tf = 1/(np.sum(drug_indications_matrix_dict[key]==1)+1)
        drug_indications_matrix_dict[key] *= indications_idf*tf

    # print(drug_indications_matrix_dict)
    with open("./drug_indications_tfidf.pickle", "wb") as wf:
       pickle.dump(drug_indications_matrix_dict, wf)



