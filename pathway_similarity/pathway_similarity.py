import pandas as pd
import pickle
import csv
import numpy as np

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
    pathway = pickle.load(open('./drug_pathway_tfidf.pickle', 'rb'))
    features_matrix = []
    drug_list = []
    features_matrix = []
    for did in pathway.keys():
        drug_list.append(did)
        fp_list = list(map(int, pathway.get(did)))
        # print(fp_list)
        features_matrix.append(fp_list)
    features_matrix = np.asarray(features_matrix)
    similarity = get_Jaccard_Similarity(features_matrix)
    similarity_df = pd.DataFrame(similarity, columns = drug_list, index = drug_list)
    print(similarity_df)
    similarity_df.to_csv("pathway_similarity.csv")

if __name__ == "__main__":
    main()
