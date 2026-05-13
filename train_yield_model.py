import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import joblib

# Load dataset
df = pd.read_csv("datasets/milk_yield.csv")

# Drop unnecessary columns
drop_cols = ["Cattle_ID", "Date", "Farm_ID"]

for col in drop_cols:
    if col in df.columns:
        df.drop(col, axis=1, inplace=True)

# Encode categorical columns
label_encoders = {}

for col in df.select_dtypes(include=["object", "string"]).columns:
    le = LabelEncoder()

    df[col] = le.fit_transform(df[col].astype(str))

    label_encoders[col] = le

# Features and target
X = df.drop("Milk_Yield_L", axis=1)
y = df["Milk_Yield_L"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=20,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy
score = r2_score(y_test, predictions)

print(f"Model Accuracy (R2 Score): {score:.2f}")

# Save model
joblib.dump(model, "models/milk_yield_model.pkl")

print("Model saved successfully!")