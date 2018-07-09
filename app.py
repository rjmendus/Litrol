from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
	return "Howdy! It's up!"

@app.route('/predict', methods=['GET','POST'])
def predict():
	if request.method == 'GET':
		return "Get method is up."
	
	return "Success"

if __name__ == "__main__":
	app.run(debug=True)