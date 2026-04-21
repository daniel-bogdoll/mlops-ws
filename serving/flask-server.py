from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/invocations', methods=['POST'])
def predict():
    inputs = request.json['inputs']
    prediction = 0
    return jsonify({'prediction': prediction}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
