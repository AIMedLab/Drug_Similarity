import numpy as np
import pandas as pd
import pickle

df1 = pickle.load(open('./approved_drug_uid.pickle', 'rb'))
# df2 = pickle.load(open('./pid2fasta.pickle', 'rb'))
# # drug_list = ["DB01076","DB00227","DB08860","DB00175","DB01098","DB00641"]
drug_list = []
for did in df1.keys():
    drug_list.append(did)

n = len(drug_list)
# print(n)


# path = '/users/PCON0023/xueqiao/temp/result_new'
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
    # print(file)
# with open("result_new_test.txt", "wb") as outfile:
#     for i in sorted_file:
#         file = path + '/' + i
#         with open(file, "rb") as infile:
#             lines = infile.readlines()  # 读取所有行
#             first_line = lines[0]
#             outfile.write(first_line)

columns = ['data']
df = pd.read_csv('result_new_test.txt', sep = '\t', header=None, names = columns)


df["data"] = df["data"].apply(lambda x: x.replace('[','').replace(']',''))
print(df)
df = df["data"].str.split(',',expand=True)
df = df.dropna(how = 'any')  
check_for_nan = df.isnull().values.any()
print(check_for_nan)
# df.values[[np.arange(df.shape[0])]*2] = 0
df.columns = drug_list
df.index = drug_list
# print(df)
df.to_csv("sequence_similarity.csv")
