import numpy as np
import pandas as pd
import pickle
import os

df1 = pickle.load(open('./did2pid_new.pickle', 'rb'))
# # df2 = pickle.load(open('./pid2fasta.pickle', 'rb'))
# # # drug_list = ["DB01076","DB00227","DB08860","DB00175","DB01098","DB00641"]
drug_list = []
for did in df1.keys():
    drug_list.append(did)

n = len(drug_list)
print(n)


# path = './cc_result'
# path = './mf_result'
# path = './bp_result'
# fileslist = os.listdir(path)

# sort_num_list = []
# for file in fileslist:
#     sort_num_list.append(int(file.split('result')[1].split('.txt')[0])) 
#     sort_num_list.sort() 
    
# print(len(sort_num_list))

# sorted_file = []
# for sort_num in sort_num_list:
#     for file in fileslist:
    
#         if str(sort_num) == file.split('result')[1].split('.txt')[0]:
#             sorted_file.append(file)
# print(sorted_file)           
# print(len(sorted_file))
# for i in sorted_file:
#     file = path + '/' + i
#     print(file)
# with open("./cc_similarity.txt", "wb") as outfile:
# with open("./bp_similarity.txt", "wb") as outfile:
# with open("./mf_similarity.txt", "wb") as outfile:
#     for i in sorted_file:
#         file = path + '/' + i
#         with open(file, "rb") as infile:
#             lines = infile.readlines() 
#             print(len(lines)) # 读取所有行
#             print(file)
#             first_line = lines[0]
#             outfile.write(first_line)

columns = ['data']
df = pd.read_csv('./cc_similarity.txt', sep = '\t', header=None, names = columns)
# df = pd.read_csv('./mf_similarity.txt', sep = '\t', header=None, names = columns)
# df = pd.read_csv('./bp_similarity.txt', sep = '\t', header=None, names = columns)


df["data"] = df["data"].apply(lambda x: x.replace('[','').replace(']',''))
df = df["data"].str.split(',',expand=True)
df = df.dropna(how= 'any') 
check_for_nan = df.isnull().any()

print(check_for_nan)
# df = df.fillna(0)
# # df.values[[np.arange(df.shape[0])]*2] = 0
df.columns = drug_list
df.index = drug_list
# df = df.apply(pd.to_numeric)
print(df.dtypes)
print(df)
df.to_csv("./Go_cc_similarity.csv")
# df.to_csv("./Go_mf_similarity.csv")
# df.to_csv("./Go_bp_similarity.csv")



# print(df)
