# Drug_Similarity
------------------
## 1. Introduction
This repository contains implementation code of different drug similarities computing. Currently, we have six drug similarities include chemical, protein sequence, indication, pathway, ATC code and GO terms similarities of 1787 approved drugs.

## 2. Pipeline
Figure1: Overall framework for the drug similarity computing.
## 3. Usage

### ATC code similarity 
We define the *k*th level ATC code based similarity *S~k* of drug *a* and drug *b* as      
![atc_1](https://latex.codecogs.com/svg.image?S_k(a,b)=\frac{ATC_k(a)\cap&space;ATC_k(b)}{ATC_k(a)\cup&space;ATC_k(b)})
