import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Get path to the current script
script_dir = Path(__file__).parent

# Build path to train.csv relative to the script
train_path = script_dir.parent / "data" / "train.csv"

train_df = pd.read_csv(train_path)

def create_features(data_frame):
    data_frame = pd.get_dummies(data_frame, columns=["customerType"], dtype=int, drop_first=True)
    data_frame["orderedBooks"] = data_frame["basket"].apply(lambda x: sum(c.isdigit() for c in x))
    return data_frame

train_df = create_features(train_df)

features = ["totalAmount", "orderedBooks"] 
scaler = StandardScaler()
train_df[features] = scaler.fit_transform(train_df[features])

x_train = train_df.drop(columns=["returnLabel", "transactionId", "basket"])
y_train = train_df["returnLabel"]

params = {"n_estimators": 100, "max_features": "sqrt", "random_state": 0}
rf = RandomForestClassifier(**params)
rf.fit(x_train, y_train)

test_path = script_dir.parent / "data" / "test.csv"
test_df = pd.read_csv(test_path)
test_df = create_features(test_df)
features = ["totalAmount", "orderedBooks"]
test_df[features] = scaler.transform(test_df[features])
X_test = test_df.drop(["transactionId", "returnLabel", "basket"], axis=1)
predictions = rf.predict(X_test)
y_test = test_df["returnLabel"]
print("Accuracy :", accuracy_score(y_test, predictions))
print("Precision:", precision_score(y_test, predictions))
print("Recall   :", recall_score(y_test, predictions))

joblib.dump(rf, script_dir.parent / "models" / "model.pkl", compress=9)
joblib.dump(scaler, script_dir.parent / "models" / "scaler.pkl", compress=9) 
