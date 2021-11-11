#!/bin/python

import os
import sys
import getopt

argv=sys.argv[1:]
#print(argv)

try:
    opts, args = getopt.getopt(argv,"hx:y:")
except:
    print ('run_wasp_gen.py -x <x> -y <y>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print ('run_wasp_gen.py -x <x> -y <y>')
        sys.exit()
    elif opt in ("-x"):
        x_file = arg
    elif opt in ("-y"):
        y_file = arg

os.system("python3 generate_snp_info.py -x %s -y %s" % (x_file,y_file))

with open ("y_metadata_file.txt",'r') as f:
    data=f.read().rstrip().split()
    num_individuals=data[0]
os.system("python3 generate_all_other_info.py -y y_metadata_file.txt")
os.system('python3 generate_read_counts.py -l l_inv_file.txt -n %s -i individual_info.txt' % (num_individuals))
#prina(x_file)
