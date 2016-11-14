from Globals import filenames_PC as filenames

def random_matrix(size):
    from numpy.random import random, randint
    from numpy import array, float64
    
    with open(filenames['random'],'rb') as file1:
        if size%259993 == 0:
            print 'Error: No staggering'
        matrix = [float(line[:-1])+1 for line in file1]
        start = randint(0,len(matrix)-1)
        matrix = matrix*(size/len(matrix)+1)
        matrix = matrix[start:] + matrix[:start]
    return array(matrix[:size], dtype=float64)


def find_signatures(data, rank=50, beta=0.1, eta=0.1, threshold=0.01):
    from Read_data import replace_placeholder
    from numpy import array, nanmean, dot, multiply, product, copy, identity
    from numpy import concatenate, zeros, ones, isnan
    from numpy.linalg import norm
    from math import sqrt

    V = replace_placeholder(data, value = 0.00001)
    data_positions = ~isnan(data)
    #V = multiply(data, data_positions)
    data_positions_H = concatenate((copy(data_positions), ones((len(V),rank))),
                                   axis=1)
    data_positions_W = concatenate((copy(data_positions), ones((1,len(V.T)))))

    def update_W(V, W, H):
        Term_1 = dot(V, H.T)
        Term_2 = dot(multiply(dot(W, H),data_positions_H), H.T)
        return multiply(multiply(W,Term_1), 1./Term_2)


    def update_H(V, W, H):
        Term_3 = dot(W.T, V)
        Term_4 = dot(W.T, multiply(dot(W, H),data_positions_W))
        return multiply(multiply(H,Term_3), 1./Term_4)


    # Normalize columns of W so that L2-norm of each column =1 and throw the
    # scale factor into rows of H.
    def W_normalize(W, H):
        return array([W[:,i]/norm(W[:,i]) for i in range(W.shape[1])]).T, \
               array([H[i]*norm(W[:,i]) for i in range(H.shape[0])])


    def SNMF():
        W_shape = (len(V), rank)
        H_shape = (rank, len(V.T))
        print 'Initializing W and H...'
        W = random_matrix(product(W_shape)).reshape(W_shape)
        H = random_matrix(product(H_shape)).reshape(H_shape)
        print 'W, H chosen'
        error_old = 0
        error_new = 100
        iterations = 0
        while abs(error_old-error_new) > threshold or iterations<150:
            H1 = concatenate((copy(H), sqrt(eta)*identity(rank)), axis=1)
            V1 = concatenate((copy(V), zeros((len(V),rank))),axis=1)
            W = update_W(V1, W, H1)

            W2 = concatenate((copy(W), sqrt(beta)*ones((1,rank))))
            V2 = concatenate((copy(V), zeros((1,len(V.T)))))
            H = update_H(V2, W2, H)

            error_old = error_new
            error_new = norm(V-multiply(dot(W,H),data_positions))/norm(V)*100
            W, H = W_normalize(W, H)
            print 'Iteration ',iterations,', Error = ', error_old
            iterations += 1
        return array(W), array(H), error_new

    return SNMF() # returns [array(W), array(H), error_new]

def read_W():
    from numpy import array
    with open(filenames['W'], 'rb') as readfile:
        W = readfile.readlines()
    return array([map(float, line.split()) for line in W])


from Read_data import read_full_link_json
full_link_ids, V = read_full_link_json(trips=0)
W, H, error = find_signatures(V, rank=50, beta=0.1, eta=0.1, threshold=0.01)
print W.shape, H.shape

print full_link_ids[1]
from pickle import load
sig_dis = load(open('Data_Files/Signature_Distribution.p','rb'))
print sig_dis[full_link_ids[1]]
from matplotlib.pyplot import plot, show
Wfile = open('Data_Files/W.txt','rb')
W = read_W()
[plot(range(24), W[i*24:(i+1)*24,35]) for i in range(7)]
show()















