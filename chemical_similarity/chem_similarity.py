import pubchempy as pcp
import pandas as pd
import pickle
import csv
import numpy as np

# df = pd.read_csv("../../drugparse/data/drugbank/drugbank_pubchem.csv")

def get_Jaccard_Similarity(interaction_matrix):
    X = np.mat(interaction_matrix)
    E = np.ones_like(X.T)
    denominator=X * E + E.T * X.T - X * X.T
    denominator_zero_index=np.where(denominator==0)
    denominator[denominator_zero_index]=1
    result = X * X.T / denominator
    result[denominator_zero_index]=0
    result = result - np.diag(np.diag(result))

    return result


def main():
    did2fp = pickle.load(open('./did2fp.pickle', 'rb'))
    drug_list = []
    features_matrix = []
    for did in did2fp.keys():
        drug_list.append(did)
        fp_list = list(map(int, did2fp.get(did)))
        features_matrix.append(fp_list)
    features_matrix = np.asarray(features_matrix)
    # print(features_matrix)
    similarity = get_Jaccard_Similarity(features_matrix)
    similarity_df = pd.DataFrame(similarity, columns = drug_list, index = drug_list)
    print(similarity_df)
    similarity_df.to_csv("chem_similarity.csv")


# def main():
#     did2fp = pickle.load(open('./did2fp.pickle', 'rb'))
#     features_matrix = []
#     drug_list = ["DB01076","DB00227","DB08860","DB00175","DB01098","DB00641"]
#     for did in drug_list:
#         fp_list = list(map(int, did2fp.get(did)))
#         print(fp_list)
#         features_matrix.append(fp_list)
#     features_matrix = np.asarray(features_matrix)
#     similarity = get_Jaccard_Similarity(features_matrix)
#     similarity_df = pd.DataFrame(similarity, columns = drug_list, index = drug_list)
#     print(similarity_df)
#     # np.savetxt("/users/PCON0023/xueqiao/drugsimilarity/drugparse/data/result/chem_similarity_test.csv", similarity_df, delimiter=",")
#     similarity_df.to_csv("/users/PCON0023/xueqiao/drugsimilarity/drugparse/data/result/chem_similarity_test.csv")

if __name__ == "__main__":
    main()
