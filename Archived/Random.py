from numpy.random import random, randint
from time import time
from numpy import array

def random_matrix(size):
    with open('./Data_Files/Reorganized/Random_numbers.txt','r') as file1: 
        matrix = []
        init  = randint(1,260000)
        for i in range(init):
            file1.readline()
        for i in range(size):
            entry = file1.readline()[:-1]
            if bool(entry):
                matrix.append(float(entry))
            else:
                file1.seek(0)
                entry = file1.readline()[:-1]
                matrix.append(float(entry))
        return array(matrix)
