from Globals import *
filenames = filenames_PC
 

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

# Make HT sparser by flattening out things below half-peak height in
# each row of HT.
def axe_H(HT0):
    from numpy import copy, array
    HT = copy(HT0)
    for i in range(len(HT0)):
        peak  = max(HT0[i])
        HT[i] = [entry if entry>peak/2. else 0. for entry in HT0[i]]
    return array(HT)


# Sort H and W according to decreasing order of signature popularity
# which is calculted using H obtained from axe_H().
def sort_WH(W0, H0):
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

    popularity, H, WT = zip(*[(pop,row_H,col_W) for (pop,row_H,col_W)
                              in sorted(zip(popularity,H0,W0.T),
                                        key=lambda pair: pair[0], reverse=True)])
    W = array(WT).T
    H = array(H)
    return W, H
        

def find_signatures(data, rank=RANK, beta=0.1, threshold=0.2, seed_W=None,
                    seed_H=None):
    from Read_data import replace_placeholder
    from numpy import array, nanmean, dot, multiply, product, copy, identity
    from numpy import zeros, ones, isnan, amin, diag
    from numpy import sum as npsum
    from numpy.linalg import norm
    from math import sqrt, log
    from matplotlib.pyplot import plot, show

    print 'Rank=', rank, 'Beta=', beta, 'Threshold=', threshold 
    D = replace_placeholder(data, value = 0.0)
    data_positions = ~isnan(data)
    
    def update_W(D, W, H):
        # diag(diag(A)) replaces all off-diagonal entries of A with 0.
        Term_1 = dot(D, H.T)
            
        Term_2 = dot(multiply(dot(W, H),data_positions), H.T)+\
                 dot(W,diag(diag(dot(W.T,dot(D,H.T)))))-\
                 dot(W,diag(diag(dot(dot(W.T,multiply(\
                     data_positions,dot(W,H))),H.T))))
                 
        return multiply(multiply(W,Term_1), 1./Term_2)

    def update_H(D, W, H):
        Term_3 = dot(W.T, D)
        Term_4 = dot(W.T, multiply(dot(W, H),data_positions))\
                 + beta*dot(ones((rank,rank)), H)
        return multiply(multiply(H,Term_3), 1./Term_4)

    def quartiles(H):
        H2 = sorted(H.flatten())
        return H2[0], H2[(rank*FULL_LINKS-1)/4], H2[(rank*FULL_LINKS-1)*2/4],\
               H2[(rank*FULL_LINKS-1)*3/4], H2[rank*FULL_LINKS-1] 

    def SNMF():
        W_shape = (len(D), rank)
        H_shape = (rank, len(D.T))
        print 'Initializing W and H...'
        W = random_matrix(product(W_shape), seed_W).reshape(W_shape)
        H = random_matrix(product(H_shape), seed_H).reshape(H_shape)
        print 'W, H chosen'
        iterations = 0
        quarts = [] # list of quartiles for each iteration
        diff_W = 100
        diff_H = 100
        diff = []
        errors = []
        W_mins = []
        W_maxs = []
        while abs(diff_W) + abs(diff_H) > threshold or iterations<200:
            W_new = update_W(D, W, H)
            H_new = update_H(D, W_new, H)

            W_mins.append(W_new.min())
            W_maxs.append(W_new.max())
            diff.append((diff_W, diff_H))

            diff_W = norm(W_new-W)/norm(W)*100
            diff_H = norm(H_new-H)/norm(H)*100

            print 'diff_W = ', diff_W, ', diff_H = ', diff_H

            W, H = W_new, H_new

            # We calculate the relative error in percentage.
            error = norm(D-multiply(dot(W,H),data_positions))/norm(D)*100
            print 'Iteration ', iterations, ', Error = ', error
            iterations += 1
            errors.append(error)
            quarts.append(quartiles(H))

        plot(W_maxs)
        plot(W_mins)
        show()

        [plot([entry[i] for entry in diff[3:]], 'o-') for i in range(2)]
        plot(errors[3:],'o-')
        show()

        W, H = sort_WH(W, H)
        print 'Sparsity=' , 1./(product(H_shape))*sum(array(
            [norm((coeffs-max(coeffs))/max(coeffs))**2 for coeffs in H.T]))
        quarts = array(quarts).T
        [plot(quarts[i],'o-') for i in range(5)]
        show()
        
        return W, H, error

    return SNMF() # returns [array(W), array(H), error]



from Read_data import read_full_link_json
from numpy import savetxt
full_link_ids, D = read_full_link_json() # Reads trips or traveltimes
                                         # depending on Globals.TRIPS value 
print 'Full_link data has been read'

if SEEDED == 1:
    seed_W = 0
    seed_H = 1
elif SEEDED == 0:
    seed_W = None
    seed_H = None
else:
    print 'Seed value invalid. Needs to be 0 or 1. Check Globals.py!'
    quit()
    
W, H, error = find_signatures(D, rank=RANK, seed_W=seed_W, seed_H=seed_H)

if TRIPS == 1:
    savetxt(filenames['W_trips'], W)
    print 'W_trips written'
    savetxt(filenames['HT_trips'], H.T)
    print 'HT_trips written'
    savetxt(filenames['HT_trips_axed'], axe_H(H.T))
    print 'HT_trips_axed written'
elif TRIPS == 0:
    savetxt(filenames['W_traveltimes'], W)
    print 'W_travel_times written'
    savetxt(filenames['HT_traveltimes'], H.T)
    print 'HT_travel_times written'
    savetxt(filenames['HT_traveltimes_axed'], axe_H(H.T))
    print 'HT_travel_times_axed written'

