'''
1) sample from N(0, Lam^-1). It's trivial to ignore the mean here. You can add the mean to run our model on the data. 
2) apply the standard normal cumulative dist Phi(z) on the samples in 1)
3) apply F^-1(samples from 2)), where F is the cumulative dist of univariate neg binomial. 
'''
#lam-1 passed in 
from tables import *
import sys
import numpy as np
from scipy import stats
import getopt
n=0
lambda_file=''
chromosome_name='chr22'
argv=sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hl:n:i:")
except getopt.GetoptError:
    print ('generate_read_counts.py -l <lambda_inv_file> -n <num_samples> -i <individuals_file>')
    sys.exit(2) 
for opt, arg in opts:
    if opt == '-h':
        print ('generate_read_counts.py -l <lambda_inv_file> -n <num_samples> -i <individuals_file>')
        sys.exit()
    elif opt in ("-l"):
        lambda_file = arg
    elif opt in ("-n"):
        n = int(arg)
    elif opt in ("-i"):
        ind_file=arg

with open(ind_file) as f:
    ind_list=f.readlines()
ind_list=[x.split()[0] for x in ind_list]
l=np.loadtxt(lambda_file,delimiter=" ")
two_q=len(l)
noiseY = np.random.multivariate_normal(np.zeros(two_q), l, size=n)
cdf=stats.norm.cdf(noiseY)
epsilon=1
mean=np.zeros((n,two_q))+epsilon
variance=np.tile(np.diag(l)+epsilon,(n,1))
p=np.divide(mean,variance)
r=np.divide(mean**2,variance-mean)
read_counts=np.array([stats.nbinom.ppf(cdf[i],r[i],p[i]) for i in range(len(cdf))]).reshape((2*n,-1))
read_counts=read_counts[::2,:]+read_counts[1::2,:]
#split 50-50
alt_read_counts=read_counts//2
ref_read_counts=read_counts-alt_read_counts
# other is currently all 0
other_read_counts=np.zeros((n,two_q//2))
c=0
for ind in ind_list:
    alt_read_count_file='alt_as_counts.'+ind+'.h5'
    h5file = open_file(alt_read_count_file, mode="w", title="alt read count test file")
    ref_read_count_file='ref_as_counts.'+ind+'.h5'
    h5file.create_array("/", chromosome_name,alt_read_counts[c].astype('uint16'))
    h5file.close()
    h5file = open_file(ref_read_count_file, mode="w", title="ref read count test file")
    h5file.create_array("/", chromosome_name,ref_read_counts[c].astype('uint16'))
    h5file.close()
    other_read_count_file='other_as_counts.'+ind+'.h5'
    h5file = open_file(other_read_count_file, mode="w", title="other read count test file")
    h5file.create_array("/", chromosome_name,other_read_counts[c].astype('uint16'))
    h5file.close()
    read_count_file='read_counts.'+ind+'.h5'
    h5file = open_file(read_count_file, mode="w", title="read count test file")
    h5file.create_array("/", chromosome_name,read_counts[c].astype('uint16'))
    h5file.close()
    c+=1
