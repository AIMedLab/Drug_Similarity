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
    df = np.count_nonzero(input_metric) 
    idf = np.log((drug_size + 1) / (df + 1)) 
    # print("idf:", "max:", np.max(idf), "min:", np.min(idf))
    return np.transpose(idf)


def get_feature_matrix():
    didenzyme = pickle.load(open('./drug_enzyme.pickle', 'rb'))
    actions = pickle.load(open('./enzyme_inhibitor.pickle', 'rb'))   
    drug_size = len(didenzyme)
    #get all the drugs
    all_drug_list = list(didenzyme.keys())
    #get all enzymes
    all_enzymes_list = list(set(sum(didenzyme.values(),[])))
    #get all enzymes have actions
    inhibitor_enzymes_list = list(actions.keys())
    all_enzymes_list.sort()
    matrix_size = len(all_enzymes_list)
    
    drug_enzymes_matrix_dict = {}
    for drug in didenzyme:
        if drug not in drug_enzymes_matrix_dict:
            drug_enzymes_matrix_dict[drug] = np.zeros(matrix_size)
        for enzymes in didenzyme[drug]:
            if enzymes in inhibitor_enzymes_list:
                drug_enzymes_matrix_dict[drug][all_enzymes_list.index(enzymes)] = -1
            else: 
                drug_enzymes_matrix_dict[drug][all_enzymes_list.index(enzymes)] = 1     
        

    return drug_enzymes_matrix_dict, drug_size, matrix_size, all_enzymes_list


if __name__ == '__main__':

    drug_enzymes_matrix_dict, drug_size, matrix_size, all_enzymes_list = get_feature_matrix()
    enzymes_idf = calculate_IDF(drug_enzymes_matrix_dict, drug_size, matrix_size)
    print("drug size:", drug_size, "  matrix_size:", matrix_size)
    # print(drug_enzymes_matrix_dict['DB14487'])
    # one-hot coding ==> idf matrix
    for key in drug_enzymes_matrix_dict.keys():
        tf = 1/(np.sum(drug_enzymes_matrix_dict[key]==1)+1)
        drug_enzymes_matrix_dict[key] *= (enzymes_idf * tf)

    # print(drug_enzymes_matrix_dict)
    with open("./drug_enzymes_tfidf.pickle", "wb") as wf:
       pickle.dump(drug_enzymes_matrix_dict, wf)



