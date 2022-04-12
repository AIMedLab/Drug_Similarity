import pandas as pd
import pickle
import csv
import numpy as np

def get_Cosin_Similarity(interaction_matrix):
    X = np.mat(interaction_matrix)
    alpha = np.multiply(X, X).sum(axis=1)
    similarity_matrix = X * X.T / (np.sqrt(alpha * alpha.T))
    similarity_matrix[np.isnan(similarity_matrix)] = 0
    for i in range(similarity_matrix.shape[0]):
        similarity_matrix[i, i] = 0

    return similarity_matrix

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
    enzymes = pickle.load(open('./drug_enzymes_tfidf.pickle', 'rb'))
    features_matrix = []
    drug_list = []
    features_matrix = []
    for did in  enzymes.keys():
        drug_list.append(did)
        fp_list = list(map(int, enzymes.get(did)))
        # print(fp_list)
        features_matrix.append(fp_list)
    features_matrix = np.asarray(features_matrix)
    similarity = get_Jaccard_Similarity(features_matrix)
    similarity_df = pd.DataFrame(similarity, columns = drug_list, index = drug_list)
    print(similarity_df)
    similarity_df.to_csv("enzymes_similarity_jaccard.csv")

if __name__ == "__main__":
    main()
