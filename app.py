from flask import Flask, request, jsonify
import json
import numpy as np 
import pandas as pd
import time
from keras.models import model_from_json
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

@app.route('/')
def home():
	return "Howdy! It's up!"

@app.route('/predict', methods=['GET'])
def predict():
	if request.method == 'GET':
		predicted_price =  str(predict_petrol_price())
		print("Tomorrow's price",predicted_price)
		return jsonify(
			Price=predicted_price
		)
	else:
		return "Not authorised."
	return "Success"

@app.route('/getprice', methods=['GET'])
def get_price():
	if request.method == 'GET':
		df = pd.read_csv('static/dataset/DelhiPrice.csv')
		return jsonify(
			Price=str(df['Weighted_Price'][0])
		)
	else:
		return "Not authorised."

@app.route('/uploadmodeljson', methods=['GET','POST'])
def upload_model_json():
	if request.method == 'POST':
		uploaded_json = request.get_json()
		with open('static/models/model.json', 'w') as outfile:
			json.dump(uploaded_json, outfile)
		return "200"

	return "Error"

def predict_petrol_price():

	sc = MinMaxScaler()
	df = pd.read_csv('static/dataset/DelhiPrice.csv')
	df['date'] = pd.to_datetime(df['Timestamp'],unit='s').dt.date
	group = df.groupby('date')
	Real_Price = group['Weighted_Price'].mean()
	prediction_days = 30
	df_train= Real_Price[:len(Real_Price)-prediction_days]
	df_test= Real_Price[len(Real_Price)-prediction_days:]
	training_set = df_train.values
	training_set = np.reshape(training_set, (len(training_set), 1))
	training_set = sc.fit_transform(training_set)
	# load json and create model
	json_file = open('static/models/model.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model.load_weights("static/models/model.h5")
	print("Loaded model from disk")
	# Fitting the RNN to the Training set
	regressor=loaded_model
	# Making the predictions
	test_set = df_test.values
	print("test Values",test_set)
	inputs = np.reshape(test_set, (len(test_set), 1))
	inputs = sc.transform(inputs)
	print(sc.inverse_transform(inputs),type(inputs))
	inputs = np.reshape(inputs, (len(inputs), 1, 1))
	predicted_Petrol_price = regressor.predict(inputs)
	predicted_Petrol_price = sc.inverse_transform(predicted_Petrol_price)
	print("Predicted Price\n",predicted_Petrol_price)
	predicted_Petrol_price = predicted_Petrol_price.tolist()
	print(predicted_Petrol_price[-1][0])
	return predicted_Petrol_price[-1][0]

if __name__ == "__main__":
	app.run(debug=True)