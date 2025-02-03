from flask import Flask, jsonify

app = Flask(__name__)

# Define a simple route
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Define an API endpoint that returns JSON data
@app.route('/api', methods=['GET'])
def greet():
    return jsonify(stink="Hello, welcome to my API!")

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
