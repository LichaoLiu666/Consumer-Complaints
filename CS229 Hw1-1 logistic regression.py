'''
problem 1.b
Develop the logistic regression newton method optimization
'''
import numpy as np
import os
import math
from numpy.linalg import inv

os.chdir('C:/Users/J046314/Documents/IPython Notebooks/ML')


with open('q1x.dat') as f:
    X_temp = np.array([line.split() for line in f],dtype=float) 
    X= np.insert(X_temp, 0, [1]*99, axis=1)
with open('q1y.dat') as f:
    y = np.array([line.split() for line in f],dtype=float)



def logit(x):
    return 1/(1+math.exp(x)**-1)

def cost(X,y,theta):
    return sum(y*np.log(np.array(list(map(logit,np.dot(X,theta)))).reshape(99,1))+ (1-y)*np.log(1-np.array(list(map(logit,np.dot(X,theta)))).reshape(99,1)))

def gradient(X,y,theta):
    return (sum(((list(map(logit,np.dot(X,theta)))-y.T)[0]*X.T).T)/len(y)).reshape(3,1)
    
def hessian(X,y,theta):
    w=np.diag(list((np.array(list(map(logit,np.dot(X,theta)))).reshape(1,99)*np.array(list(map(lambda x:1-logit(x),np.dot(X,theta)))).reshape(1,99))[0]))
    return np.dot(np.dot(X.T,w),X)/len(y)
    

def newton(X,y,theta,tol=.5,max_itr=50):
    itr=0
    while abs(cost(X,y,theta))[0]>tol and itr<=max_itr:
        theta=theta-np.dot(inv(hessian(X,y,theta)),gradient(X,y,theta))
        itr+=1
    return theta,cost(X,y,theta)

theta=np.array([[0],[0],[0]])

newton(X,y,theta)

#Sklearn logistic-------------------------
from sklearn import linear_model
logit_model=linear_model.LogisticRegression(fit_intercept=True)
logit_model.fit(X, y)
logit_model.coef_

#optimization with scipy----------------------------
from scipy.optimize import minimize
res=minimize(cost,theta,method='nelder-mead',options={'xtol': 1e-8, 'disp': True})
#==============================================================================
# Problem 1.c plot data
import matplotlib.pyplot as plt

coef=newton(X,y,theta)
h=.01
x_min, x_max = X[:, 1].min() - .5, X[:, 1].max() + .5
y_min, y_max = X[:, 2].min() - .5, X[:, 2].max() + .5
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))


Z=np.exp(coef[0][0]+coef[0][1]*xx.ravel()+coef[0][2]*yy.ravel())>.5
Z = Z.reshape(xx.shape)

fig, ax = subplots()
ax.contourf(xx, yy, Z,cmap='RdBu', alpha=.5)
plt.scatter(X[:,1],X[:,2], marker='o', c=y)


#==============================================================================
