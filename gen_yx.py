import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as ssp
import scipy.sparse.linalg as ssl
import sys

#sys.path.append("../Mega-sCGGM/")
from mega_scggm import mega_scggm
from q_mega_scggm import q_mega_scggm

n = 5
m = 2
p = 3
q = 3
nan_percent_col=0.0
#r = 5

X=np.random.choice(2,(n,2*p))
print (X.shape)
A=ssp.random(q,q)
Omega=A.T@A+0.01*ssp.identity(q)
Xnew=X.reshape((2*n,-1))
Xsum= Xnew[::2,:]+Xnew[1::2,:]

#q*q
Delta=ssp.eye(q, format="coo")
Delta.setdiag(0.3, 0)

Pi=ssp.rand(p,q)
Xi=ssp.rand(p,q)
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

x_file='x_file'
y_file='y_file'
lambda_inv_file='lambda_inv_file'
np.savetxt(x_file,Xnew,delimiter=" ")
np.savetxt(y_file,Y,delimiter=" ")
np.savetxt(lambda_inv_file,Sigma.todense(),delimiter=' ')