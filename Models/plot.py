from pandas import read_csv, datetime
from matplotlib import pyplot 

def parser(x):
	return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

def plot_original_and_prediction(yhat, athlete):
	# used in rio_predictions
	dataset = read_csv('csv_dates.csv', header=0, index_col=0, date_parser=parser)
	ax = dataset['distance'].plot()
	ax.set_ylabel('Distance (m)')
	ax.set_xlabel('Date')
	ax.set_title(athlete[0] + " " + athlete[1])
	# print(dataset.index)
	ax.plot(dataset.index[-yhat.shape[0]:],yhat, 'r')
	ax.legend(['Actual', 'Predicted'])
	pyplot.show()

# # plot values for single athlete (raw data)
# dataset = read_csv('csv_dates.csv', header=0, index_col=0, date_parser=parser)
# ax = dataset['distance'].plot()
# ax.set_ylabel('Distance (m)')
# ax.set_xlabel('Date')
# ax.set_title('Kristiina Makela')
# pyplot.show()