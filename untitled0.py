# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vkQrhN3dPGuwwkRAwOzhxcufXtiW9Mxl
"""

#It uses an artificial recurrent neural network called Long Short Term Memory(LSTM)
# to predict the closing stock price of a corporation(Apple Inc). using the past 60 days stock price.

#Import the libraries
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#get the stock code
df = web.DataReader('AAPL', data_source='yahoo', start= '2012-01-01', end='2019-12-17')
#show the data
df

import pandas_datareader as web
import datetime

# Convert the date strings to datetime objects
start_date = datetime.datetime(2012, 1, 1)
end_date = datetime.datetime(2019, 12, 17)

# Get the historical stock data for AAPL
df = web.DataReader('AAPL', data_source='yahoo', start=start_date, end=end_date)

# Show the data
print(df)

import yfinance as yf

# Define the ticker symbol and date range
ticker_symbol = 'AAPL'
start_date = '2012-01-01'
end_date = '2019-12-17'

# Fetch historical data using yfinance
df = yf.download(ticker_symbol, start=start_date, end=end_date)

# Show the data
print(df)

#get the number of rows and columns
df.shape

#visualize the closing price history
plt.figure(figsize=(16,18))
plt.title('Close Price History')
plt.plot(df['Close'])
plt.xlabel('date', fontsize=18)
plt.ylablel('Close Price USD($)', fontsize=18)
plt.show()

#Create a new dataframe with only the close column
data = df.filter(['Close'])
#convert the dataframe to a numpy
dataset = data.values
#get the number of rows to train the model on
training_data_len = math.ceil(len(dataset) * 0.8)

training_data_len

#scale the data
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

scaled_data

#create the training dataset
#create the scaled training dataset
train_data = scaled_data[0:training_data_len, :]
#split the data into x_train sets
x_train = []
y_train = []

for i in range(60, len(train_data)):
  x_train.append(train_data[i-60:i, 0])
  y_train.append(train_data[i, 0])
  if i<=60:
    print(x_train)
    print(y_train)
    print()

#convert x_train and y_train to numpy arrays
x_train , y_train = np.array(x_train), np.array(y_train)

#Reshape the data
x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
x_train.shape

#build the LSTM model
#model = Sequential()
#model.add(LSTM(50, return_sequence=True, input_shape =(x_train.shape[1],1)))
#model.add(LSTM(50,return_sequence=False))
#model.add(Dense(25))
#model.add(Dense(1))
# Build the LSTM model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))  # No need for 'return_sequences' in the last LSTM layer
model.add(Dense(25))
model.add(Dense(1))

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Create a Sequential model
model = Sequential()

# Add the first LSTM layer with 50 units and return_sequences=True
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))

# Add a second LSTM layer with 50 units and return_sequences=False
model.add(LSTM(50, return_sequences=False))

# Add a Dense layer with 25 units
model.add(Dense(25))

# Add the output layer with 1 unit (for regression tasks)
model.add(Dense(1))

# Create the scaled training dataset
train_data = scaled_data[0:training_data_len, :]

# Initialize lists for input (x_train) and output (y_train)
x_train = []
y_train = []

# Loop to create sequences
for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])

#Compile the model
#from tensorflow.keras.models import Model
#Model.compile(optimizer='adam', loss='mean_squared_error')
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError

# Define your custom model class (replace with your actual model architecture)
class MyModel(tf.keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        # Define your model layers here

# Create an instance of your model
model = MyModel()

# Compile the model
model.compile(optimizer=Adam(), loss=MeanSquaredError())

#Train the model
#model.fit(x_train,y_train,batch_size=1, epochs=1)
import numpy as np

# Assuming x_train and y_train are lists or arrays
x_train = np.array(x_train)  # Convert x_train to a NumPy array
y_train = np.array(y_train)  # Convert y_train to a NumPy array

# Reshape x_train if needed (assuming it's a 2D array)
x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)

# Train the model
model.fit(x_train, y_train, batch_size=1, epochs=1)

import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense

class MyModel(tf.keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.lstm1 = LSTM(50, return_sequences=True)
        self.lstm2 = LSTM(50, return_sequences=False)
        self.dense1 = Dense(25)
        self.dense2 = Dense(1)

    def call(self, inputs):
        x = self.lstm1(inputs)
        x = self.lstm2(x)
        x = self.dense1(x)
        x = self.dense2(x)
        return x

# Create an instance of your custom model
model = MyModel()

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(x_train, y_train, batch_size=1, epochs=1)

#Create the testing dataset
#create a new array containg scaled values from 1543 to 2003
test_data=scaled_data[training_data_len-60:]
#create the data sets c_test anf y_test
x_test=[]
y_test=dataset[training_data_len:, :]
for i in range(60, len(test_data)):
  x_test.append(test_data[i-60:i, 0])

#Convert the data to a numpy array
x_test = np.array(x_test)

#reshape the data
x_test = np.reshape(x_test,(x_test.shape[0], x_test.shape[1],1))

#het the models predicted price values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

#het the models predicted price values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

import numpy as np  # Import the NumPy library

# Reshape predictions to be a 2D array
predictions = predictions.reshape(-1, 1)

# Inverse transform the scaled predictions
predictions = scaler.inverse_transform(predictions)

#het the models predicted price values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

import numpy as np

# Assuming predictions has shape (batch_size, sequence_length, num_features)
# Reshape predictions to (batch_size * sequence_length, num_features)
predictions = predictions.reshape(-1, 1)

# Inverse transform the scaled predictions
predictions = scaler.inverse_transform(predictions)

#get the root mean squared error(RMSE)
rmse = np.sqrt(np.mean(predictions-y_test)**2)
rmse

import numpy as np

# Assuming predictions and y_test have the following shapes:
# predictions shape: (400, 60, 1)
# y_test shape: (400, 1)

# Reshape predictions to (400, 60)
#predictions = predictions.reshape(-1, 60)

# Calculate the RMSE for each prediction
#rmse = np.sqrt(np.mean((predictions - y_test)**2, axis=1))

# Calculate the overall RMSE (you can use np.mean to get the average RMSE)
#overall_rmse = np.mean(rmse)

#print("Overall RMSE:", overall_rmse)

import numpy as np

# Assuming predictions and y_test have the following shapes:
# predictions shape: (400, 60, 1)
# y_test shape: (400, 1)

# Calculate the RMSE for each prediction
rmse = np.sqrt(np.mean((predictions - y_test)**2, axis=1))

# Calculate the overall RMSE (you can use np.mean to get the average RMSE)
overall_rmse = np.mean(rmse)

print("Overall RMSE:", overall_rmse)

#plot the data
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions
#visualise the data
plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train','Val','Predictions'], loc='lower right')
plt.show()

# Assuming you have already calculated predictions as mentioned earlier

# Create a new DataFrame for predictions
predictions_df = pd.DataFrame(predictions, columns=['Predictions'], index=valid.index)

# Concatenate the 'valid' DataFrame with 'predictions_df'
valid = pd.concat([valid, predictions_df], axis=1)

# Plot the data
plt.figure(figsize=(16, 8))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid['Close'])
plt.plot(valid['Predictions'])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.show()

# Assuming you have already calculated predictions as mentioned earlier

# Convert the DatetimeIndex to a NumPy array and reshape it
#index_array = valid.index.to_numpy().reshape(-1, 1)

# Create a new DataFrame for predictions
#predictions_df = pd.DataFrame(predictions, columns=['Predictions'], index=index_array)

# Concatenate the 'valid' DataFrame with 'predictions_df'
##valid = pd.concat([valid, predictions_df], axis=1)

# Plot the data
#plt.figure(figsize=(16, 8))
#plt.title('Model')
#plt.xlabel('Date', fontsize=18)
#plt.ylabel('Close Price USD ($)', fontsize=18)
#plt.plot(train['Close'])
#plt.plot(valid['Close'])
#plt.plot(valid['Predictions'])
#plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
#plt.show()
# Check and confirm that the indices of 'valid' and 'predictions_df' match
if valid.index.equals(predictions_df.index):
    # Indices match, so it's safe to concatenate
    valid = pd.concat([valid, predictions_df], axis=1)

    # Plot the data as in your original code
    plt.figure(figsize=(16, 8))
    plt.title('Model')
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price USD ($)', fontsize=18)
    plt.plot(train['Close'])
    plt.plot(valid['Close'])
    plt.plot(valid['Predictions'])
    plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
    plt.show()
else:
    # Handle the case where indices don't match (e.g., perform index alignment or resampling)
    print("Indices do not match. Please align or resample the data.")

# Assuming you have already calculated predictions as mentioned earlier

# Create a new DataFrame for predictions with the same index as 'valid'
predictions_df = pd.DataFrame(index=valid.index[-len(predictions):])

# Assign the 'Predictions' column
predictions_df['Predictions'] = predictions

# Concatenate the 'valid' DataFrame with 'predictions_df'
valid = pd.concat([valid, predictions_df], axis=1)

# Plot the data
plt.figure(figsize=(16, 8))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid['Close'])
plt.plot(valid['Predictions'])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.show()

# Assuming you have already calculated predictions as mentioned earlier

# Create a new DataFrame for predictions with the same index as 'valid'
predictions_df = pd.DataFrame(index=valid.index[-len(predictions):])

# Assign the 'Predictions' column
predictions_df['Predictions'] = predictions

# If the 'Predictions' column already exists, replace it
if 'Predictions' in valid.columns:
    valid['Predictions'] = predictions_df['Predictions']
else:
    # Concatenate the 'valid' DataFrame with 'predictions_df'
    valid = pd.concat([valid, predictions_df], axis=1)

# Plot the data
plt.figure(figsize=(16, 8))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid['Close'])
plt.plot(valid['Predictions'])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.show()