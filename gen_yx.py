import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as ssp
import scipy.sparse.linalg as ssl
import sys
import getopt

n = 5
m = 2
p = 5
q = 5
nan_percent_col=0.0
#r = 5
argv=sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hn:p:q:",['nan_percent='])
except getopt.GetoptError:
    print ('generate_read_counts.py -n <num_samples> -p <num_SNP> -q <num_genes> --nan_percent <num_missing>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print ('generate_read_counts.py -n <num_samples> -p <num_SNP> -q <num_genes> --nan_percent <num_missing>')
        sys.exit()
    elif opt in ("-n"):
        n = int(arg)
    elif opt in ("-p"):
        p = int(arg)
    elif opt in ("-q"):
        q=int(arg)
    elif opt in ('--nan_percent'):
        nan_percent_col=float(arg)


X=np.random.choice(2,(n,2*p))
print (X.shape)
A=ssp.random(q,q)
Omega=A.T@A+0.01*ssp.identity(q)
Xnew=X.reshape((2*n,-1))
Xsum= Xnew[::2,:]+Xnew[1::2,:]

#q*q
Delta=ssp.eye(q, format="coo")
Delta.setdiag(0.3, 0)

Pi=ssp.rand(p,q,density=0.5)
Xi=ssp.rand(p,q,density=0.5)
print(Pi.toarray())
#
Lambda=ssp.kron(ssp.identity(m,format="coo"),Delta)+ssp.kron(np.ones((m,m)),Omega)
Theta=ssp.vstack([ssp.kron(ssp.identity(m,format="coo"),Pi),ssp.kron(np.ones((1,m)),Xi)])
Sigma = ssl.inv(Lambda)
meanY = -1 * np.hstack((X,Xsum)) @ Theta @ Sigma
noiseY = np.random.multivariate_normal(np.zeros(m*q), Sigma.todense(), size=n)
Y = meanY + noiseY
Ynew=Y.reshape((2*n,-1))
Ysum= Ynew[::2,:]+Ynew[1::2,:]

for i in range(q):
        l = np.random.choice(np.arange(n), replace=False, size=int(n*nan_percent_col))
        Y[l,i]=float('nan')
        Y[l,i+q]=float('nan')
theta_file='t_file.txt'
x_file='x_file.txt'
y_file='y_file.txt'
lambda_inv_file='l_inv_file.txt'
np.savetxt(theta_file,meanY,delimiter=" ")
np.savetxt(x_file,Xnew,fmt="%d",delimiter=" ")
np.savetxt(y_file,Y.reshape((2*n,-1)),delimiter=" ")
np.savetxt(lambda_inv_file,Sigma.todense(),delimiter=' ')
