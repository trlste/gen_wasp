'''
1) sample from N(0, Lam^-1). It's trivial to ignore the mean here. You can add the mean to run our model on the data. 
2) apply the standard normal cumulative dist Phi(z) on the samples in 1)
3) apply F^-1(samples from 2)), where F is the cumulative dist of univariate neg binomial. 
'''
#lam-1 passed in 
from tables import *
import sys
import numpy as np
import scipy

n=0
lambda_file=''
chromosome_name='chr22'
try:
    opts, args = getopt.getopt(argv,"hl:n:")
except getopt.GetoptError:
    print ('generate_read_counts.py -l <lambda_inv_file> -n <num_samples>')
    sys.exit(2) 
for opt, arg in opts:
    if opt == '-h':
        print ('generate_read_counts.py -l <lambda_inv_file> -n <num_samples>')
        sys.exit()
    elif opt in ("-l"):
        lambda_file = arg
    elif opt in ("-n"):
        n = arg

l=np.loadtxt(lambda_file,delimiter=" ")
two_q=len(l)
noiseY = np.random.multivariate_normal(np.zeros(two_q), l, size=n).reshape((2*n,-1))
cdf=scipy.stats.norm.cdf(noiseY)
read_counts=scipy.stats.nbinom.ppf(cdf)
read_counts=read_counts[::2,:]+read_counts[1::2,:]
#split 50-50
alt_read_counts=read_counts//2
ref_read_counts=read_counts-alt_read_counts
# other is currently all 0
other_read_counts=np.zeroes((n,two_q//2))

h5file = open_file(alt_read_count_file, mode="w", title="alt read count test file")
h5file.create_array("/", chromosome_name,alt_read_counts)
h5file.close()
h5file = open_file(ref_read_count_file, mode="w", title="ref read count test file")
h5file.create_array("/", chromosome_name,ref_read_counts)
h5file.close()
h5file = open_file(other_read_count_file, mode="w", title="other read count test file")
h5file.create_array("/", chromosome_name,other_read_counts)
h5file.close()
h5file = open_file(read_count_file, mode="w", title="read count test file")
h5file.create_array("/", chromosome_name,read_counts)
h5file.close()