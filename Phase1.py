''' This contains functions for cSNMF.
cSNMF uses L1-normalization condition for W and
also takes into account the signs of lambda_n'''


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
    #   numbers between 0 and 1.
    # * Reads numbers from pre-generated file: filenames['random'] in order
    #   to save time.
    # * seed = 1 will ensure that the same random_array is generated everytime.
    size = np.prod(shape)
    with open(filenames['random'], 'rb') as file1:
        assert size%259993 != 0         # To ensure staggeredness of filesize
        matrix = [float(line[:-1]) for line in file1]
        rand.seed(seed)
        start = rand.randint(0,len(matrix)-1) # start at a random position in the file
        matrix = matrix*(size//len(matrix)+1)
        matrix = matrix[start:] + matrix[:start]
    return np.array(matrix[:size]).reshape(shape)
    


def axe_H(H, relative_cutoff=0.5):
    # Makes H sparser by flattening out things below half-peak height in
    # each column of H.
    
    def axe_column(column):
        peak = max(column)
        return column.mask(column < peak*relative_cutoff, other = 0.0)

    return H.apply(axe_column, axis=0)


def sort_WH(W0, H0):
    # Sort H and W according to decreasing order of signature popularity
    # which is calculated using H obtained from axe_H().
    H = axe_H(pd.DataFrame(H0)).values()
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
    def sparsity_column(column):
        column = (column - column.max())/column.max()
        column = column**2
        return np.sum(column)
    return sum([sparsity_column(i) for i in H.T])/np.product(H.shape)


def factorize(dataframe, filenames, rank, beta = 0.1, threshold = 0.20, seed_W = None, seed_H = None, log=logger):    

    log.info('Rank= %s, Beta= %s, Threshold= %s', rank, beta, threshold)

    D = dataframe.fillna(0.0)
    global NONZEROS
    NONZEROS = pd.notnull(dataframe)
    JTT = np.ones((D.shape[0],D.shape[0]))
    JRR = np.ones((rank,rank))
    
    
    def update_W(D, W, H):
        WH = N(W @ H)
        DHT = D @ H.T
        WHHT = WH @ H.T
        JTTW = JTT @ W
        
        # This is a rank*rank matrix with only lambda_n on the diagonals
        lambdas = 1./D.shape[0]*np.diag(np.sum(DHT - WHHT, axis=0)) 
        #print(np.diag(lambdas[4:6,4:6]))
        Term_1 = DHT - JTTW @ np.select([lambdas < 0.], [lambdas])
        Term_2 = WHHT + JTTW @ np.select([lambdas >= 0.], [lambdas])
        W = m(m(W,Term_1), 1./(Term_2))
        #W = np.select([W > 10**(-30)], [W], default=10**(-30))    ## Bumping values back up to epsilon
        return W

    
    def update_H(D, W, H):
        WH = N(W @ H)
        
        Term_3 = W.T @ D
        Term_4 = W.T @ WH + beta*JRR @ H
        H = m(m(H,Term_3), 1./Term_4)
        #H = np.select([H > 10**(-30)], [H], default=10**(-30))
        return H
    

    def quartiles(H):
        H2 = sorted(H.flatten())
        quarter = (rank*D.shape[1]-1)//4
        return H2[0], H2[quarter], H2[quarter*2], H2[quarter*3], H2[-1] 

    
    logger.info('Initializing W and H...')
    
    W = random_array(((D.shape[0]-1), rank), filenames, seed_W)
    W.sort(axis=0)
    W = np.concatenate((np.zeros((1,rank)), W, np.ones((1,rank))))
    W = np.array([W[i+1]-W[i] for i in range(W.shape[0]-1)])
    try:
        assert np.sum(np.sum(W,axis=0)==1)==rank
    except AssertionError:
        log.critical('Assertion Error: W_initialization failed to have column sums of 1')
        raise
    
    H = random_array((rank, D.shape[1]), filenames, seed_H)
    
    log.info('W, H chosen')

    iterations = 0
    results = pd.DataFrame()
    diff_W = 100
    diff_H = 100
    
    D = D.values # DataFrame to numpy.array
    norm_D = lin.norm(D)
    
    while abs(diff_W) + abs(diff_H) > threshold or iterations<200:
        W_new = update_W(D, W, H)
        H_new = update_H(D, W_new, H)
        
        #print(np.sum(W_new[:,4]))
        try: assert(np.sum(W_new,axis=0).max()<1.2 and np.sum(W_new,axis=0).min()>0.8)
        except AssertionError:
            pass
            #log.critical('AssertionError: W col_sum out of range!')
            #log.critical('W col_sum = %s max and %s min', np.sum(W_new,axis=0).max(), np.sum(W_new,axis=0).min())
            #np.savetxt('./Debug/W_new.csv', W_new, delimiter=',')
            #np.savetxt('./Debug/H_new.csv', H_new, delimiter=',')
            #np.savetxt('./Debug/W.csv', W, delimiter=',')
            #np.savetxt('./Debug/H.csv', H, delimiter=',')
            #return pd.DataFrame(W), pd.DataFrame(H), results
            #raise
        
        #if iterations>125:
        #    from IPython.core.debugger import Tracer
        #    Tracer()()

        # Check for nonnegativity of W
        try: assert(W_new.min()>=0)
        except AssertionError:
            log.critical('AssertionError: W is not nonnegative!')
            log.critical('%s out of %s entries of W are negative', np.sum(W_new < 0), np.product(W.shape))
            return pd.DataFrame(W), pd.DataFrame(H), results
            raise

        # Check for nonnegativity of H
        try: assert(H_new.min()>=0)
        except AssertionError:
            log.critical('AssertionError: H is not nonnegative!')
            log.critical('%s out of %s entries of H are negative', np.sum(H_new < 0), np.product(H.shape))
            return pd.DataFrame(W), pd.DataFrame(H), results
            raise

        
        diff_W = lin.norm(W_new - W)/lin.norm(W)*100
        diff_H = lin.norm(H_new - H)/lin.norm(H)*100

        W, H = W_new, H_new

        # We calculate the relative error in percentage.
        error = lin.norm(D - N(W@H))/norm_D*100
        sparsity = sparsity_metric(H)
        
        log.info('Iteration= %s, Error= %s', iterations, error)
        iterations += 1
            
        results = results.append({'quarts': quartiles(H),
                                  'W_min': W.min(),
                                  'W_max': W.max(),
                                  'diff_W': diff_W,
                                  'diff_H': diff_H,
                                  'error': error,
                                  'sparsity': sparsity,
                                  'col_sum_mean': np.mean(np.sum(W,axis=0))
                                  }, ignore_index = True)
            
        
    # W, H = sort_WH(W, H)
    log.info('Sparsity= %s', sparsity)
    return pd.DataFrame(W), pd.DataFrame(H), results







