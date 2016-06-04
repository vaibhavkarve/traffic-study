from matplotlib.pyplot import show
from Data_matrix import data_matrix_create
from Daily_trends import daily_trends
from Non_negative_matrix_factorization import NMF, NMF_plot

data = data_matrix_create()
for day_index in range(7):
    daily_trends(data,day_index)
    NMF_plot(data, day=day_index)
    show()
