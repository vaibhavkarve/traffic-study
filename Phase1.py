''' This runs Phase1 on data using L1-normalization condition for W and also by taking into account the signs of lambda_n'''


from read_data import replace_placeholder
import numpy as np
import pandas as pd
import numpy.linalg as lin
import numpy.random as rand
import math
import matplotlib.pyplot as plt
import logging
import sys


logger = logging.getLogger(__name__)


## Useful matrix operations:
def m(A,B): return np.multiply(A,B)
def d(A): return np.diag(np.diag(A))  # d(A) replaces all off-diagonal entries of A with 0.
def N(A): return m(A, NONZEROS)       # NONZEROS is a global variable.


def random_array(shape, filenames, seed = None):
    # * Creates a numpy.array of specified shape and populates it with random
    #   numbers between 1 and 2.
    # * Reads numbers from pre-generated file: filenames['random'] in order
    #   to save time.
    # * seed = 1 will ensure that the same random_array is generated everytime.
    size = np.prod(shape)
    with open(filenames['random'], 'rb') as file1:
        assert size%259993 != 0         # To ensure staggeredness of filesize
        matrix = [float(line[:-1])+1 for line in file1]
        rand.seed(seed)
        start = rand.randint(0,len(matrix)-1) # start at a random position in the file
        matrix = matrix*(size//len(matrix)+1)
        matrix = matrix[start:] + matrix[:start]
    return np.array(matrix[:size]).reshape(shape)
    


def axe_H(HT0):
    # Makes HT sparser by flattening out things below half-peak height in
    # each row of HT.

    HT = np.copy(HT0)
    for i in range(len(HT0)):
        peak  = max(HT0[i])
        HT[i] = [entry if entry>peak/2. else 0. for entry in HT0[i]]
    return np.array(HT)


def sort_WH(W0, H0):
    # Sort H and W according to decreasing order of signature popularity
    # which is calculted using H obtained from axe_H().
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
    W = np.array(WT).T
    H = np.array(H)
    return W, H
        

def sparsity_metric(H):
    numer = sum(np.array([lin.norm((coeffs-max(coeffs))/max(coeffs))**2 for coeffs in H.T]))
    denom = (np.product(H.shape))
    return numer/denom



def SNMF(dataframe, filenames, rank, beta = 0.1, threshold = 0.20, seed_W = None, seed_H = None):    

    logger.info('Rank= %s, Beta= %s, Threshold= %s', rank, beta, threshold)

    D = dataframe.fillna(0.0)
    global NONZEROS
    NONZEROS = pd.notnull(dataframe)
    
    def update_W(D, W, H):
        lambdas = d(W.T@(D - N(W@H))@H.T)  # This is a rank*rank matrix with only lambda_n on the diagonals
        Term_1 = D@H.T - np.ones((len(D),len(D)))@W@np.select([lambdas < 0], [lambdas])
        Term_2 = N(W@H)@H.T + np.ones((len(D),len(D)))@W@np.select([lambdas >= 0], [lambdas])
        return m(m(W,Term_1), 1./(Term_2))

    def update_H(D, W, H):
        Term_3 = W.T@D
        Term_4 = W.T@N(W@H) + beta*np.ones((rank,rank))@H
        return m(m(H,Term_3), 1./Term_4)
    

    def quartiles(H):
        H2 = sorted(H.flatten())
        quarter = (rank*len(D.T)-1)//4
        return H2[0], H2[quarter], H2[quarter*2], H2[quarter*3], H2[-1] 


    W_shape = (D.shape[0], rank)
    H_shape = (rank, D.shape[1])
    logger.info('Initializing W and H...')
    W = random_array(W_shape, filenames, seed_W)
    H = random_array(H_shape, filenames, seed_H)
    
    logger.info('W, H chosen')

    iterations = 0
    results = pd.DataFrame({'quarts': [], # list of quartiles of H for each iteration
                            'diff_W': [],
                            'diff_H': [],
                            'error': [],
                            'W_min': [],
                            'W_max': [],
                            'sparsity': [],
                            'col_sum_mean': []})
    diff_W = 100
    diff_H = 100
    
    D = D.values # DataFrame to numpy.array
    
    while abs(diff_W) + abs(diff_H) > threshold or iterations<200:
        W_new = update_W(D, W, H)
        H_new = update_H(D, W_new, H)
        

        # Check for nonnegativity of W
        try: assert(W_new.min()>0)
        except AssertionError:
            logger.critical('AssertionError: W is not nonnegative!')
            logger.critical('%s out of %s entries of W are negative', np.sum(W_new <= 0), np.product(W_shape))
            raise

        # Check for nonnegativity of H
        try: assert(H_new.min()>0)
        except AssertionError:
            logger.critical('AssertionError: H is not nonnegative!')
            logger.critical('%s out of %s entries of H are negative', np.sum(H_new <= 0), np.product(H_shape))
            raise

        
        W_min = W_new.min()
        W_max = W_new.max()
        diff_W = lin.norm(W_new - W)/lin.norm(W)*100
        diff_H = lin.norm(H_new - H)/lin.norm(H)*100

        W, H = W_new, H_new

        # We calculate the relative error in percentage.
        error = lin.norm(D - N(W@H))/lin.norm(D)*100
        
        logger.info('Iteration= %s, Error= %s', iterations, error)
        iterations += 1
        
        results = results.append({'quarts': quartiles(H),
                                  'diff_W': diff_W,
                                  'diff_H': diff_H,
                                  'error': error,
                                  'W_min': W_min,
                                  'W_max': W_max,
                                  'sparsity': sparsity_metric(H),
                                  'col_sum_mean': np.mean(np.sum(W,axis=0))}, ignore_index = True, )
            
        
    W, H = sort_WH(W, H)
            
    return pd.DataFrame(W), pd.DataFrame(H), results







