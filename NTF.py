from numpy import array, product, tensordot, multiply, argmax, concatenate
from numpy import nan, ndarray, isnan, copy, mean, ones, zeros, identity, amax
from numpy import sum as sum2
from numpy.random import random
from math import sqrt
from Random import random_matrix

def replace_placeholder(data, placeholder = nan, value = 0):
    data_type = type(data)
    if data_type is ndarray:
        shape = data.shape
        data = list(data.flatten())
    if isnan(placeholder):
        data = [i if ~isnan(i) else value for i in data]
    else:
        data = [i if i!=placeholder else value for i in data]
    if data_type is list:
        return data
    elif data_type is ndarray:
        return array(data).reshape(shape)
    else:
        print 'Error: check type() of data\n'
        return None

def tensorprod(tensor1, tensor2, contraction):
    indices_1 = range(-contraction, 0)
    indices_2 = range(contraction-1, -1,-1)
    return tensordot(tensor1, tensor2, [indices_1, indices_2])

    
def NTF(data, RANK = 1, axis = 0, round = 0):
    D = array(data)
    shape = D.shape
    if axis >= len(shape)-1:
        print 'axis value too large.'
        return None

    D = replace_placeholder(D, value = 0.00001)
    W_shape = list(shape[0:axis+1])
    W_shape.append(RANK)
    H_shape = [RANK]
    H_shape.extend(shape[axis+1:])
    W = random_matrix(product(W_shape)).reshape(W_shape)
    H = random_matrix(product(H_shape)).reshape(H_shape)
    if round == 1:
        H[:,0] = 0.00001
        H[0,0] = 1
    for iterations in range(199):
        Term_1 = tensorprod(D, H.T, len(H.shape)-1)
        Term_2 = tensorprod(W, tensorprod(H,H.T,len(H.shape)-1), 1)
        W = multiply(multiply(W,Term_1), 1./Term_2)

        Term_3 = tensorprod(W.T, D, len(W.shape)-1)
        Term_4 = tensorprod(tensorprod(W.T,W,len(W.shape)-1), H, 1)
        H = multiply(multiply(H,Term_3), 1./Term_4)
    
        if round == 1 and iterations%100 == 99:
            for i in range(H.shape[1]):
                norms = []
                for r in range(H.shape[0]):
                    norm = tensorprod(H[r,i], H[r,i].T, len(H[r,i].shape))
                    norms.append(norm)
                r = argmax(norms)
                H[:,i] = 0.00001
                H[r,i] = 1
                #H[:,i] = floor(H[:,i]/max(H[:,i]))
        # Following is the error term, which is derived from the matrix norm.
        print sum2(multiply(D - tensorprod(W,H,1), D - tensorprod(W,H,1)))/mean(D)/D.size
        #print sum2(H.T)
    return array(W), array(H)

def SNTF(data, RANK = 1, axis = 0, beta = 0.5, eta = 0.001):
    D = array(data)
    if axis >= len(D.shape)-1:
        print 'axis value too large.'
        return None

    D = replace_placeholder(D, value = 0.0001)
    W_shape = list(D.shape[0:axis+1])
    W_shape.append(RANK)
    H_shape = [RANK]
    H_shape.extend(D.shape[axis+1:])
    W = random_matrix(product(W_shape)).reshape(W_shape)
    H = random_matrix(product(H_shape)).reshape(H_shape)
    print 'W, H chosen'
    error_old = 0
    error_new = sum2(multiply(D - tensorprod(W,H,1), D - tensorprod(W,H,1)))/mean(D)/D.size
    while abs(error_old-error_new) > 0.0001:
        D1 = concatenate((copy(D), zeros(W.shape)), axis=len(W.shape)-1)
        H1 = concatenate((copy(H), sqrt(eta)*identity(RANK)), axis=1)
        
        Term_1 = tensorprod(D1, H1.T, len(H1.shape)-1)
        Term_2 = tensorprod(W, tensorprod(H1,H1.T,len(H1.shape)-1), 1)
        W = multiply(multiply(W,Term_1), 1./Term_2)
        
        W2 = concatenate((copy(W), sqrt(beta)*ones((1,)+W.shape[1:])))
        D2 = concatenate((copy(D), zeros((1,)+D.shape[1:])))
        
        Term_3 = tensorprod(W2.T, D2, len(W2.shape)-1)
        Term_4 = tensorprod(tensorprod(W2.T,W2,len(W2.shape)-1), H, 1)
        H = multiply(multiply(H,Term_3), 1./Term_4)
        
        error_old = error_new
        error_new = sum2(multiply(D - tensorprod(W,H,1), D - tensorprod(W,H,1)))/mean(D)/D.size

        # Following is the error term, which is derived from the matrix norm.
        #print error_old# - error_new
    #print error_new*mean(D)*D.size
    #print sum2(sum2(H.T)**2)
    #print sum2(multiply(W,W))
    #return error_new*mean(D)*D.size, sum2(sum2(H.T)**2), sum2(multiply(W,W))
    #return error_new*mean(D)*D.size
    return array(W), array(H)
