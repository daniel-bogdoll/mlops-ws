from pyexpat import features

from flask import Flask, jsonify, request
from pickle import load

import pandas as pd

app = Flask(__name__)

def load_model(model_path: str):
    with open(model_path, "rb") as f:
        model = load(f)
    return model

def preprocess_input(data):

    # [{'transactionId': 9534310106, 'basket': [4, 3, 4], 'totalAmount': 100.0, 'customerType': 'new'}]
    # Convert input data to DataFrame
    data_frame = pd.DataFrame(data)

    # One Hot Encoding of Basket
    def one_hot_encode_basket(df: pd.DataFrame, unique_categories: set, column: str='basket'):
        # Find unique categories in the specified column
        unique_categories_found = set()
        for basket in df[column]:
            categories = [int(category) for category in basket]
            unique_categories_found.update(categories)

        # Check if all found unique categories are in the provided set of unique categories
        if not unique_categories_found.issubset(unique_categories):
            print("Warning: Found unique categories that are not in the provided set of unique categories.")
            print("Found unique categories:", unique_categories_found)
            print("Provided unique categories:", unique_categories)

        # Create new columns for each unique category
        unique_categories_sorted = sorted(unique_categories)
        for category in unique_categories_sorted:
            category_string = f"bookcategory_{category}"

            # Count the number of times the category appears in the specified column
            df[category_string] = df[column].apply(lambda x: x.count(str(category)))

        # Remove the original column
        df.drop(column, axis=1, inplace=True)

        return df

    #One-Hot Encoding of Customer Type
    data_frame["customerType_new"] = data_frame["customerType"].apply(lambda x: 1 if x == "new" else 0)

    data_frame["orderedBooks"] = data_frame["basket"].apply(lambda x: sum(c for c in x))

    # One-hot Encoding of Basket
    data_frame = one_hot_encode_basket(data_frame, unique_categories)

    # Drop unnecessary columns
    data_frame.drop(["transactionId", "customerType"], axis=1, inplace=True)

    return data_frame

@app.route('/invocations', methods=['POST'])
def predict():
    inputs = request.json['inputs']

    # Preprocess inputs
    inputs = preprocess_input(inputs)

    # Scale inputs
    features_for_scaling = ["totalAmount", "orderedBooks"]
    inputs[features_for_scaling] = scaler.transform(inputs[features_for_scaling])

    # Make prediction
    prediction = model.predict(inputs)
    print(f" Raw prediction: {prediction}")
    return jsonify({'prediction': prediction.tolist()}), 201

# uv run python serving/flask-server.py
if __name__ == "__main__":
    model_path = "/home/danielbogdoll/Code/mlops-ws/models/random_forest_model.pkl"
    model = load_model(model_path)
    print("Model loaded successfully.")

    scaler_path = "/home/danielbogdoll/Code/mlops-ws/models/scaler.pkl"
    scaler = load_model(scaler_path)
    print("Scaler loaded successfully.")

    unique_categories = set([0,1,2,3,4,5])
    app.run(host="0.0.0.0", port=5000)
