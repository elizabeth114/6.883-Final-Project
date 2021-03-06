import json
import csv
import datetime

from math import sqrt
from numpy import concatenate, array
from matplotlib import pyplot
from pandas import read_csv, DataFrame, Series, concat
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, LSTM, GRU, Dropout

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

def series_to_supervised_expanding_window(data):
	n_vars = 1 if type(data) is list else data.shape[1]

	#try expanding window
	df = DataFrame(data)
	window = df.expanding()
	expanding_window_df = concat([window.min(), window.mean(), window.max(), df.shift(-1)], axis=1)
	expanding_window_df.columns = ['min', 'mean', 'max', 't+1']
	expanding_window_df.dropna(inplace=True)
	# print(expanding_window_df.head(5))

	return expanding_window_df, n_vars

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
	# reframed, n_vars = series_to_supervised(values, 15, 1)
	reframed, n_vars = series_to_supervised_expanding_window(values)
	# drop columns we don't want to predict

	# split into train and test sets
	values = reframed.values


	# train_X, test_X, train_y, test_y = train_test_split(values[:,:-1,:], values[:,-1,0], test_size=0.33)
	train_X, test_X, train_y, test_y = train_test_split(values[:,:-1], values[:,-1], test_size=0.33) # for expanding window

	# reshape input to be 3D [samples, timesteps, features]
	# train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1])) # original
	# test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
	train_X = train_X.reshape((train_X.shape[0], train_X.shape[1], 1)) # swap timesteps and features
	# print(train_X[0])
	test_X = test_X.reshape((test_X.shape[0], test_X.shape[1], 1))
	print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

	model = Sequential()
	model.add(LSTM(64, input_shape=(train_X.shape[1], train_X.shape[2])))

	model.add(Dense(16))
	model.add(Dense(8))
	model.add(Dense(1))

	model.compile(loss='mae', optimizer='adam')

	history = model.fit(train_X, train_y, epochs=1000, batch_size=50, validation_data=(test_X, test_y), verbose=0, shuffle=False)
	# plot history
	# pyplot.plot(history.history['loss'], label='train')
	# pyplot.plot(history.history['val_loss'], label='test')
	# pyplot.legend()
	# pyplot.show()
	yhat = model.predict(test_X)
	# print(yhat.shape)

	test_X = test_X.reshape((test_X.shape[0], test_X.shape[1]))
	# invert scaling for forecast
	inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1)
	inv_yhat = scaler.inverse_transform(inv_yhat)
	inv_yhat = inv_yhat[:,0]
	# invert scaling for actual
	test_y = test_y.reshape((len(test_y), 1))
	inv_y = concatenate((test_y, test_X[:, 1:]), axis=1)
	inv_y = scaler.inverse_transform(inv_y)
	inv_y = inv_y[:,0]

	# calculate RMSE
	# print(inv_y, inv_yhat)
	rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
	# rmse = sqrt(mean_squared_error(test_y, yhat))

	print('Test RMSE: %.3f' % rmse)
	return yhat

def do_the_stuff_one_net(x_data, y_data, rio_x):
	# final model
	train_X, test_X, train_y, test_y = train_test_split(x_data, y_data, test_size=0.1)

	train_X = array(train_X)
	test_X = array(test_X)
	train_y = array(train_y)
	test_y = array(test_y)
	rio_x = array(rio_x)

	train_X = train_X.reshape((train_X.shape[0], train_X.shape[1], 1))
	test_X = test_X.reshape((test_X.shape[0], test_X.shape[1], 1))
	rio_x = rio_x.reshape((rio_x.shape[0], rio_x.shape[1], 1))

	model = Sequential()
	model.add(LSTM(128, activation="relu"))
	# model.add(Dropout(0.2))
	model.add(Dense(16))
	model.add(Dense(8))
	model.add(Dense(1))
	model.compile(loss='mae', optimizer='adam')

	print(train_X.shape, train_y.shape, test_X.shape, test_y.shape, rio_x.shape)

	history = model.fit(train_X, train_y, epochs=1000, batch_size=64, validation_data=(test_X, test_y), verbose=2)
	yhat = model.predict(rio_x)

	return yhat
