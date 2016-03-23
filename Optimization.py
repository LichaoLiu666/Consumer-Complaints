import numpy as np
from scipy.optimize import minimize

def lognormal_pdf(x,theta):
    return 1/np.sqrt(2*np.pi*theta[1]**2)*np.exp(-1/2*(np.log(x)-theta[0])**2/theta[1]**2)
def lognormal_cdf(x,theta):
    return norm.cdf((np.log(x)-theta[0])/theta[1])
    
#need to minimize the obj
random_x=np.random.lognormal(mean=10, sigma=1.0, size=2000)
random_x=random_x[random_x>10000]
def obj(theta):
    return -sum([lognormal_pdf(i,theta) for i in random_x])+len(random_x)*np.log(1-lognormal_cdf(10000,theta))

result=minimize(obj,[10,1],method='Nelder-Mead',constraints=cons,options={'xtol': 1e-5, 'disp': True})
