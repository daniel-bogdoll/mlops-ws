from flask import Flask, jsonify, request
import joblib
from pathlib import Path

app = Flask(__name__)

# Get path to root directory of repo
repo_root_dir = Path(__file__).parent.parent

classifier = joblib.load(repo_root_dir / "models" / "model.pkl")
scaler = joblib.load(repo_root_dir / "models" / "scaler.pkl")

@app.route('/invocations', methods=['POST'])
def predict():
    
    inputs = request.json['inputs']
    
    totalAmount = inputs[0]["totalAmount"]
    customerType_new = inputs[0]["customerType_new"]
    orderedBooks = inputs[0]["orderedBooks"]

    scaled_features = scaler.transform([[totalAmount, orderedBooks]])
    totalAmount_scaled, orderedBooks_scaled = scaled_features[0]
    data_point = [totalAmount_scaled, customerType_new, orderedBooks_scaled]

    prediction_array = classifier.predict([data_point])
    prediction = int(prediction_array[0])

    return jsonify({'prediction': prediction}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
