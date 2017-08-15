print(a)
'''
def random_array(size, seed = None):
    # * Creates a 1-D array of specified size and populates it with random
    #   numbers between 0 and 1.
    # * Reads numbers from pre-generated file: filenames['random'] in order
    #   to save time.
    # * seed = 1 will ensure that the same random_array is generated everytime.
    
    from numpy.random import random, randint
    from numpy.random import seed as seed_func 
    from numpy import array, float64
    
    with open(filenames['random'], 'rb') as file1:
        assert size%259993 != 0         # To ensure staggeredness of filesize
        matrix = [float(line[:-1])+1 for line in file1]
        seed_func(seed)
        start = randint(0,len(matrix)-1) # start at a random position in the file
        matrix = matrix*(size/len(matrix)+1)
        matrix = matrix[start:] + matrix[:start]
    return array(matrix[:size], dtype=float64)

def axe_H(HT0):
    # Makes HT sparser by flattening out things below half-peak height in
    # each row of HT.

    from numpy import copy, array
    HT = copy(HT0)
    for i in range(len(HT0)):
        peak  = max(HT0[i])
        HT[i] = [entry if entry>peak/2. else 0. for entry in HT0[i]]
    return array(HT)


def sort_WH(W0, H0):
    # Sort H and W according to decreasing order of signature popularity
    # which is calculted using H obtained from axe_H().

    from numpy import array
    H = axe_H(H0.T).T
    column_entries = [0 for i in range(len(H.T))] # list of length 2302
    for i in range(len(H)): # i varies from 0 to 49
        for j in range(len(H.T)): # j varies from 0 to 2301
            if H[i,j] != 0:
                column_entries[j] += 1 # Counts number of nonzero entries
                                       # in each column of H

    # Calculate popularity
    popularity = []
    for i in range(len(H)):
        popularity.append(0)
        for j in range(len(H.T)):
            if H[i,j] != 0:
                popularity[i] += 1./column_entries[j]
    import numpy as np
    popularity, H, WT = zip(*[(pop,row_H,col_W) for (pop,row_H,col_W)
                              in sorted(zip(popularity,H0,W0.T),
                                        key=lambda pair: pair[0], reverse=True)])
    W = array(WT).T
    H = array(H)
    return W, H
        


def find_signatures(data, rank = config.RANK, beta = 0.1, threshold = 0.20, seed_W = None, seed_H = None):
    from Read_data import replace_placeholder
    from numpy import array, nanmean, dot, multiply, product, copy, identity
    from numpy import zeros, ones, isnan, amin, diag
    from numpy import sum as npsum
    from numpy.linalg import norm
    from math import sqrt, log
    from matplotlib.pyplot import plot, show

    print('Rank=', rank, 'Beta=', beta, 'Threshold=', threshold) 
    D = replace_placeholder(data, value = 0.0)
    data_positions = ~isnan(data)
    
    def update_W(D, W, H):
        # diag(diag(A)) replaces all off-diagonal entries of A with 0.
        Term_1 = dot(D, H.T)
            
        Term_2 = dot(multiply(dot(W, H), data_positions), H.T) + \
                 dot(W,diag(diag(dot(W.T,dot(D,H.T))))) - \
                 dot(W,diag(diag(dot(dot(W.T,multiply(\
                     data_positions,dot(W,H))),H.T))))
                 
        return multiply(multiply(W,Term_1), 1./Term_2)

    def update_H(D, W, H):
        Term_3 = dot(W.T, D)
        Term_4 = dot(W.T, multiply(dot(W, H), data_positions)) \
                 + beta*dot(ones((rank,rank)), H)
        return multiply(multiply(H,Term_3), 1./Term_4)

    def quartiles(H):
        H2 = sorted(H.flatten())
        return H2[0], H2[(rank*FULL_LINKS-1)/4], H2[(rank*FULL_LINKS-1)*2/4],\
               H2[(rank*FULL_LINKS-1)*3/4], H2[rank*FULL_LINKS-1] 

    def SNMF():
        W_shape = (len(D), rank)
        H_shape = (rank, len(D.T))
        print('Initializing W and H...')
        W = random_matrix(product(W_shape), seed_W).reshape(W_shape)
        H = random_matrix(product(H_shape), seed_H).reshape(H_shape)

        import numpy as np
        W = np.divide(W, 250)
        print('W, H chosen')

        iterations = 0
        quarts = [] # list of quartiles for each iteration
        diff_W = 100
        diff_H = 100
        diff = []
        errors = []
        W_mins = []
        W_maxs = []
        sparsity =[]
        Norms = []
        Beta_factor = []
        
        while abs(diff_W) + abs(diff_H) > threshold or iterations<200:
            W_new = update_W(D, W, H)
            H_new = update_H(D, W_new, H)

            W_mins.append(W_new.min())
            W_maxs.append(W_new.max())
            diff.append((diff_W, diff_H))

            diff_W = norm(W_new-W)/norm(W)*100
            diff_H = norm(H_new-H)/norm(H)*100

            print('diff_W = ', diff_W, ', diff_H = ', diff_H)

            W, H = W_new, H_new
            s=1./(product(H_shape))*sum(array(
            [norm((coeffs-max(coeffs))/max(coeffs))**2 for coeffs in H.T]))

            # We calculate the relative error in percentage.
            error = norm(D-multiply(dot(W,H),data_positions))/norm(D)*100
            print('Iteration ', iterations, ', Error = ', error)
            iterations += 1
            errors.append(error)
            quarts.append(quartiles(H))
            sparsity.append(s)
            Norms.append(norm(D-multiply(dot(W,H), data_positions))**2)
            Beta_factor.append(beta*sum([norm(H[:,l],1)**2 for l in range(2302)]))
        plot(Norms)
        plot(Beta_factor)
        plot(array(Norms) + array(Beta_factor))
        plot(array(Norms) - array(Beta_factor))    
        show()
        

        plot(W_maxs)
        plot(W_mins)
        show()

        [plot([entry[i] for entry in diff[3:]], 'o-') for i in range(2)]
        plot(errors[3:],'o-')
        show()

        W, H = sort_WH(W, H)
        
        quarts = array(quarts).T
        [plot(quarts[i],'o-') for i in range(5)]
        show()

        plot(sparsity)
        show()
        
        return W, H, error

    return SNMF() # returns [array(W), array(H), error]
'''