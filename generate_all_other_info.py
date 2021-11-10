#!/usr/bin/python3
'''
This file generates chrom_info, individuals, and samples files
For our purposes, individuals and samples are the same?
'''
import sys
import random
from shutil import copyfile
import getopt
chromosome_name='chr22'
argv=sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hy:")
except getopt.GetoptError:
    print ('generate_all_other_info.py -y <y_metadata_file>')
    sys.exit(2) 
for opt, arg in opts:
    if opt == '-h':
        print ('generate_all_other_info.py -y <y_metadata_file>')
        sys.exit()
    elif opt in ("-y"):
        y = arg

with open (y,'r') as f:
    data=f.read().rstrip().split()
    num_individuals=data[0]
    num_genes=data[1]

#generate chrom_info
with open('chrom_info.txt','w') as f:
    f.write(chromosome_name+" "+str(num_genes)+'\n')

#generate individual_info
with open('individual_info.txt','w') as f:
    for i in range(int(num_individuals)):
        identifier=random.randint(10000, 100000)
        f.write(str(identifier)+'\n')

#generate sample_info
copyfile('./individual_info.txt', './sample.txt')

