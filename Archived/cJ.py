from numpy import array, dot, ones, diag, around
from numpy import multiply as mp
from numpy.linalg import norm
import Globals
filenames = Globals.filenames_PC

def random_matrix(size, seed = None):
    from numpy.random import random, randint
    from numpy.random import seed as seed_func 
    from numpy import array, float64
    
    with open(filenames['random'],'rb') as file1:
        # 'random' is a file that has a list of random numbers
        # between 0 and 1 
        assert size%259993 != 0
        matrix = [float(line[:-1])+1 for line in file1]
        seed_func(seed)
        start = randint(0,len(matrix)-1) # start at a random position in the file
        matrix = matrix*(size/len(matrix)+1)
        matrix = matrix[start:] + matrix[:start]
    return array(matrix[:size], dtype=float64)

W = array([[1,0],[2,0],[3,1]])
H = array([[5,1,2,0],[1,1,1,3]])
D = dot(W,H)*10
T, L = D.shape
rank = 2
W = random_matrix(T*rank).reshape(T,rank)
H = random_matrix(rank*L).reshape(rank,L)
J = ones((T,L))
beta = 0.05

c = 0

for iterations in range(100):
    #c = sum(sum(D-dot(W,H)))/float(T*L)
    E = D-dot(W,H)-c*J

    T1 = dot(D,H.T)
    T2 = dot(W, diag(diag(dot(dot(W.T,E),H.T))))
    T3 = dot(dot(W,H),H.T) + c*dot(J,H.T)
    W = mp(W, mp(T1, 1./(T2+T3)))

    #c = sum(sum(D-dot(W,H)))/float(T*L)

    T4 = dot(W.T,D)
    T5 = dot(W.T,dot(W,H)) + beta*dot(ones((rank,rank)),H) + c*dot(W.T,J)

    H = mp(H, mp(T4,1./T5))
    
    print iterations, c, norm(E)/norm(D)*100
    
print around(dot(W,H/10.)+c*J,1),'\n'
print D/10.
print '\n\n'
print around(W,1),'\n'
print around(H/10.,1)
