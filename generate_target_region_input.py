#!/usr/bin/python3
#chromosome_name='chr22'
#allele_1='T'
#allele_2='C'
import tables
import sys

try:
    opts, args = getopt.getopt(argv,"h",["snp_tab=","snp_ind=","chrom_info="])
except getopt.GetoptError:
    print ('generate_snp_info.py -xm <x_maternal> -xp <x_paternal> -ym <y_maternal>')
    sys.exit(2) 
for opt, arg in opts:
    if opt == '-h':
        print ('generate_snp_info.py -xm <x_maternal> -xp <x_paternal> -ym <y_maternal>')
        sys.exit()
    elif opt in ("-xm"):
        xm_file = arg
    elif opt in ("-xp"):
        xp_file = arg
    elif opt in ("-ym"):
        ym_file = arg

with open('chrom_info.txt','r') as f:
    data=f.read().rstrip().split()
    chr_name=data[0]
    length=data[1]

snp_tab_h5 = tables.open_file('snp_tab.h5', "r")
snp_ind_h5= tables.open_file('snp_index.h5', "r")
snp_tab=snp_tab_h5.get_node("/%s"+chr_name)
snp_ind=snp_ind_h5.get_node("/%s"+chr_name)
with open('target_region_input.txt','w') as f:
    for item in snp_tab.iterrows():
        allele1=item['allele1']
        allele2=item['allele2']
        name=item['name']
        pos=item['pos']
        start_pos=
        end_pos=
        f.write("%s %d %d %s %s + %s %d %d\n" % (chromosome_name,pos+1,pos+1,allele1,allele2,'name',start_pos,end_pos))