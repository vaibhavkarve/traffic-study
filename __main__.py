from Data_matrix import *
from Daily_trends import *
from Non_negative_matrix_factorization import*

from matplotlib.pyplot import *

data = data_matrix_create('./Data_Files/Traveltimes_AC_2011.txt')
W, H = NMF(data)
print data.shape, W.shape, H.shape
