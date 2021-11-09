#!/usr/bin/python3

'''
This file generates snp_tab, snp_index, geno_prob and haplotype
'''

import sys
import numpy as np 
from tables import *
from np.random import default_rng
import getopt

x_file = ''
y_file = ''
argv=sys.argv[1:]
haplotype_file='haplotypes.h5'
snp_tab_file='snp_tab.h5'
snp_ind_file='snp_index.h5'
geno_prob_file='geno_probs.h5'
chromosome_name='chr22'
allele_1='T'
allele_2='C'

try:
    opts, args = getopt.getopt(argv,"hx:y:")
except getopt.GetoptError:
    print ('generate_snp_info.py -x <x> -y <y>')
    sys.exit(2) 
for opt, arg in opts:
    if opt == '-h':
        print ('generate_snp_info.py -x <x> -y <y>')
        sys.exit()
    elif opt in ("-xm"):
        x_file = arg
    elif opt in ("-y"):
        y_file = arg

class SNP():
    name = StringCol(16)
    pos = Int64Col()
    allele1 = StringCol(32)
    allele2 = StringCol(32)

x=np.loadtxt(x_file,delimiter=" ")
y=np.loadtxt(y_file,delimiter=" ")


(num_samples,num_snp)=xm.shape
(_,num_genes)=y.shape

with open('y_metadata_file.txt','w') as f:
    f.write(str(num_samples//2)+" "+str(num_genes))

#haplotype file
haplotype=x.T
h5file = open_file(haplotype_file, mode="w", title="Haplotype test file")
h5file.create_array("/", chromosome_name,haplotype)
h5file.close()


#snp_index file
#generate random positions for each SNP
rng = default_rng()
snp_positions=rng.choice(num_genes, size=num_snp, replace=False)
#generate array where each index is either -1 or corresponding SNP position in chromosome
snp_ind=[]
snp_counter=0
for i in range(num_genes):
    if i not in snp_positions:
        snp_ind.append(-1)
    else:
        snp_ind.append(snp_counter)
        snp_counter+=1

h5file = open_file(snp_ind_file, mode="w", title="Snp ind test file")
h5file.create_array("/", chromosome_name,snp_ind)
h5file.close()

#snp_tab file (name,pos,allele1, allele2)
snp_tab_name=[str(i) for i in range(num_snp)]
h5file = open_file(snp_tab_file, mode="w", title="Snp table test file")
table=h5file.create_table('/',chromosome_name,SNP)
snp_row=table.row
for i in range(num_snp):
    snp_row['name']=snp_tab_name[i]
    snp_row['pos']=snp_positions[i]
    snp_row['allele1']=allele_1
    snp_row['allele2']=allele_2
    snp_row.append()
table.flush()
h5file.close()

#genotype_prob file
xsum=(x[::2,:]+x[1::2,:]).T
def bincount2D_vectorized(a):    
    N = a.max()+1
    a_offs = a + np.arange(a.shape[0])[:,None]*N
    return np.bincount(a_offs.ravel(), minlength=a.shape[0]*N).reshape(-1,N)
counts=bincount2D_vectorized(xsum)
counts_sum=np.sum(counts,axis=1)
geno_prob=numpy.divide(counts,counts_sum)
h5file = open_file(geno_prob_file, mode="w", title="genotype prob test file")
h5file.create_array("/", chromosome_name,geno_prob)
h5file.close()

