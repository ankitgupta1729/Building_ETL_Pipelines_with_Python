import pandas
import numpy

# Dask dataframe mimics Pandas

import dask.dataframe as dd
df=dd.read_csv("anomaly.csv")
print(df.head())
#print(df.groupby(df.Power).value.mean().compute())

# dask array mimimcs numpy
# import dask.array as da
# f=h5py.file("myfile.hdf5")
# x=da.from_array(['/big_data'],chunks=(1000,1000))
# x=x.mean(axis=1).compute()

from numba import njit
import random

@njit
def monte_carlo_pi(nsamples):
	acc=0
	for i in range(nsamples):
		x=random.random()
		y=random.random()
		if (x**2 + y**2) < 1.0:
			acc +=1
	return 4.0*acc/nsamples

pi_value=monte_carlo_pi(1000)
print(pi_value)