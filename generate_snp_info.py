#!/usr/bin/python3

'''
This file generates snp_tab, snp_index, geno_prob and haplotype
'''

import sys
import numpy as np 
from tables import *
from numpy.random import default_rng
import getopt

x_file = ''
y_file = ''
argv=sys.argv[1:]
#print(argv)
haplotype_file='haplotypes.h5'
snp_tab_file='snp_tab.h5'
snp_ind_file='snp_index.h5'
geno_prob_file='geno_probs.h5'
chromosome_name='chr22'
allele_1='T'
allele_2='C'

try:
    opts, args = getopt.getopt(argv,"hx:y:")
except:
    print ('generate_snp_info.py -x <x> -y <y>')
    sys.exit(2) 
for opt, arg in opts:
    if opt == '-h':
        print ('generate_snp_info.py -x <x> -y <y>')
        sys.exit()
    elif opt in ("-x"):
        x_file = arg
    elif opt in ("-y"):
        y_file = arg
#print(x_file)

class SNP(IsDescription):
    name = StringCol(16)
    pos = Int64Col()
    allele1 = StringCol(32)
    allele2 = StringCol(32)

x=np.loadtxt(x_file,delimiter=" ")
y=np.loadtxt(y_file,delimiter=" ")


(num_samples,num_snp)=x.shape
(_,num_genes)=y.shape

with open('y_metadata_file.txt','w') as f:
    f.write(str(num_samples//2)+" "+str(num_genes))

#haplotype file
haplotype=x.T
h5file = open_file(haplotype_file, mode="w", title="Haplotype test file")
h5file.create_array(h5file.root, chromosome_name,haplotype)
#h5file
h5file.close()


#snp_index file
#generate random positions for each SNP
rng = default_rng()
snp_positions=rng.choice(num_genes, size=num_snp, replace=False)
#generate array where each index is either -1 or corresponding SNP position in chromosome
snp_ind=[]
print(snp_positions)
for i in range(num_genes):
    if i not in snp_positions:
        snp_ind.append(-1)
    else:
        snp_ind.append(np.where(snp_positions == i)[0][0])
print(snp_ind)
h5file = open_file(snp_ind_file, mode="w", title="Snp ind test file")
h5file.create_array(h5file.root, chromosome_name,np.array(snp_ind))
h5file.close()

#snp_tab file (name,pos,allele1, allele2)
snp_tab_name=[str(i) for i in range(num_snp)]
h5file = open_file(snp_tab_file, mode="w", title="Snp table test file")
table=h5file.create_table(h5file.root,chromosome_name,SNP)
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
geno_prob=np.array([0.25,0.5,0.25])
geno_prob=np.tile(geno_prob,(num_snp,num_samples//2))
h5file = open_file(geno_prob_file, mode="w", title="genotype prob test file")
h5file.create_array(h5file.root, chromosome_name,geno_prob)
h5file.close()
