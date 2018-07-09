from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return "Howdy! It's up!"

if __name__ == "__main__":
	app.run(debug=True)