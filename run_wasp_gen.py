#!/bin/python

import os
import sys
import getopt
import tables
import chromosome
import chromstat

argv=sys.argv[1:]
#print(argv)

try:
    opts, args = getopt.getopt(argv,"hx:y:",['target_region_size=','min_as_count=','min_read_count=','min_het_count=','min_minor_allele_count='])
except:
    print ('run_wasp_gen.py -x <x> -y <y> --target_region_size --min_as_count --min_read_count --min_het_count --min_minor_allele_count')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print ('run_wasp_gen.py -x <x> -y <y>  --target_region_size --min_as_count --min_read_count --min_het_count --min_minor_allele_count')
        sys.exit()
    elif opt in ("-x"):
        x_file = arg
    elif opt in ("-y"):
        y_file = arg
    elif opt in ("--target_region_size"):
        d=arg
    elif opt in ("--min_as_count"):
        min_as_count=arg
    elif opt in ("--min_read_count"):
        min_read_count=arg
    elif opt in ("--min_het_count"):
        min_het_count=arg
    elif opt in ("--min_minor_allele_count"):
        min_minor_allele_count=arg

os.system("python3 generate_snp_info.py -x %s -y %s" % (x_file,y_file))

with open ("y_metadata_file.txt",'r') as f:
    data=f.read().rstrip().split()
    num_individuals=data[0]
os.system("python3 generate_all_other_info.py -y y_metadata_file.txt")
os.system('python3 generate_read_counts.py -l l_inv_file.txt -n %s -i individual_info.txt' % (num_individuals))

os.system("python3 get_target_regions.py --target_region_size %s --min_as_count %s --min_read_count %s --min_het_count %s --min_minor_allele_count %s --chrom chrom_info.txt --read_count_dir ./read_counts --individuals individual_info.txt --samples sample.txt --snp_tab snp_tab.h5 --snp_index snp_index.h5 --haplotype haplotypes.h5 --output_file chr22.peaks.txt.gz" % (d,min_as_count,min_read_count,min_het_count,min_minor_allele_count))



with open("individual_info.txt") as f:
    data=f.readlines()
for item in data:
    item=item.rstrip() 
    os.system("python3 extract_haplotype_read_counts.py --chrom chrom_info.txt --snp_index snp_index.h5 --snp_tab snp_tab.h5 --geno_prob geno_probs.h5 --haplotype haplotypes.h5 --samples sample.txt --individual "+item+" --ref_as_counts read_counts/ref_as_counts."+item+".h5 --alt_as_counts read_counts/alt_as_counts."+item+".h5 --other_as_counts read_counts/other_as_counts."+item+".h5 --read_counts read_counts/read_counts."+item+".h5  chr22.peaks.txt.gz | gzip > step_6/haplotype_read_counts."+item+".txt.gz")

os.system("find step_6 -type f -name haplotype_read_counts* > step_9_input.txt")

os.system("python3 fit_as_coefficients.py step_9_input.txt cht_as_coef.txt")

os.system("python3 fit_bnb_coefficients.py --min_counts %s --min_as_counts %s step_9_input.txt cht_bnb_coef.txt" % (min_read_count,min_as_count))

os.system("python3 combined_test.py --min_as_counts %s --bnb_disp cht_bnb_coef.txt --as_disp cht_as_coef.txt step_9_input.txt cht_results.txt" % (min_as_count))
#prina(x_file)
