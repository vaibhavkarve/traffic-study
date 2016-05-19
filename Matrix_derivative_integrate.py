from numpy import *

#x=matrix(ones(30).reshape(5,6))
#x[1]=[2,2,3,3,4,4]

x=matrix(random.random_integers(1,100,(10,6)))

y=matrix([average(x[i]) for i in range(x.shape[0])]).T
z=matrix(ones(x.shape[1]))
E=x-y*z

def mat_derivative(A):
    return concatenate([A.T[i+1]-A.T[i] for i in range(A.shape[1]-1)],axis=0).T

def mat_integrate(dA,v):
    A=[v]
    for i in range(dA.shape[1]):
        A.append(A[i]+dA.T[i])
    return concatenate(A).T


#print "x=",x,"\n"
#print "y=",y,"\n"
#print "z=",z,"\n"
#print y*z,"\n"

print E
print average(E)

dE=mat_derivative(E)
print dE, average(dE)
print mat_integrate(dE,E.T[0])

