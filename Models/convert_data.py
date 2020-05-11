import json
import csv
import datetime

from math import sqrt
import numpy as np
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame, Series
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
	cols, names, cols2 = list(), list(), list() # cols2 to handle >1 features
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		# cols.append(df.shift(i))
		cols2.append(DataFrame(df.shift(i).values.flatten('F')))
		names += [('(t-%d)' % (i))] # edited by pat
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		# cols.append(df.shift(-i))
		cols2.append(DataFrame(df.shift(-i).values.flatten('F')))
		if i == 0:
			names += [('(t)')]
		else:
			names += [('(t+%d)' % (i))]
	# put it all together
	# agg = concat(cols, axis=1)
	agg = concat(cols2, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg, n_vars # edited by pat

def do_the_stuff():
	# load dataset
	dataset = read_csv('csv_dates.csv', header=0, index_col=0)
	# print(dataset)
	values = dataset.values
	# integer encode direction
	encoder = LabelEncoder()
	# ensure all data is float
	values = values.astype('float32')
	# normalize features
	scaler = MinMaxScaler(feature_range=(0, 1))
	scaled = scaler.fit_transform(values)
	# frame as supervised learning
	reframed, n_vars = series_to_supervised(values, 9, 1)
	# drop columns we don't want to predict

	# split into train and test sets
	values = reframed.values
	values = values.T
	values = values.reshape((values.shape[0], n_vars, int(values.shape[1]/n_vars))).transpose((2,0,1)) # edited by pat, turns into (samples, timesteps, features)
	# print(values)
	# print(values.shape)

	n_train_hours = len(values) - 30
	train = values[:n_train_hours]
	test = values[n_train_hours:]
	# print('trainshape', train.shape)

	# split into input and outputs
	# train_X, train_y = train[:, :-1], train[:, -1] # original
	# test_X, test_y = test[:, :-1], test[:, -1]
	train_X, train_y = train[:,:-1,:], train[:,-1,0]
	test_X, test_y = test[:,:-1,:], test[:,-1,0]

	# reshape input to be 3D [samples, timesteps, features]
	# train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1])) # original
	# test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
	# train_X = train_X.reshape((train_X.shape[0], train_X.shape[1], 1)) # swap timesteps and features
	# print(train_X[0])
	# test_X = test_X.reshape((test_X.shape[0], test_X.shape[1], 1))
	print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

	model = Sequential()
	model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))

	model.add(Dense(1))
	model.add(Dense(1))
	model.add(Dense(1))

	model.compile(loss='mae', optimizer='adam')

	history = model.fit(train_X, train_y, epochs=1500, batch_size = 50, validation_data=(test_X, test_y), verbose=2, shuffle=False)
	# plot history
	# pyplot.plot(history.history['loss'], label='train')
	# pyplot.plot(history.history['val_loss'], label='test')
	# pyplot.legend()
	# pyplot.show()
	yhat = model.predict(test_X)
	print(yhat.shape)

	# test_X = test_X.reshape((test_X.shape))#[0], test_X.shape[1]))
	# print(test_X.shape)
	# # invert scaling for forecast
	# inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1) # am i changing this correctly?
	# print(inv_yhat.shape)
	# inv_yhat = scaler.inverse_transform(inv_yhat)
	# inv_yhat = inv_yhat[:,0]
	# # invert scaling for actual
	# test_y = test_y.reshape((len(test_y), 1))
	# inv_y = concatenate((test_y, test_X[:, 1:]), axis=1)
	# inv_y = scaler.inverse_transform(inv_y)
	# inv_y = inv_y[:,0]
	# calculate RMSE
	# rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
	
	rmse = sqrt(mean_squared_error(test_y, yhat))
	print('Test RMSE: %.3f' % rmse)
	return yhat
