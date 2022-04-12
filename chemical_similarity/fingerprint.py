import pandas as pd
import pickle
from PyFingerprint.All_Fingerprint import get_fingerprint
#import numpy as np
df = pd.read_csv("drugbank_smiles.csv")
df = df.dropna(axis = 0,how = 'any')
smi_list = df["smiles"].tolist()
drug_list = df["drugbank_id"].tolist()
fingerprintList=[]
for i in range(len(smi_list)):
    fps = get_fingerprint(smi_list[i], fp_type='pubchem')
    stringFingerprint = ""
    for i in range (0,881):##Specify here the length of your fingerprint
        if i in fps:
            stringFingerprint+="1"
        else:
            stringFingerprint+="0"
    fingerprintList.append(stringFingerprint)

did2fp = dict(zip(drug_list, fingerprintList))   

with open("did2fp.pickle", "wb") as wf:
    pickle.dump(did2fp, wf)