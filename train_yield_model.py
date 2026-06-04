import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
import joblib

# Load dataset
df = pd.read_csv("datasets/milk_yield.csv")
print(df["Previous_Week_Avg_Yield"].describe())

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
X = df[
    [
        "Age_Months",
        "Weight_kg",
        "Feed_Quantity_kg",
        "Water_Intake_L",
        "Ambient_Temperature_C",
        "Humidity_percent",
        "Previous_Week_Avg_Yield"
    ]
]
y = df["Milk_Yield_L"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train XGBoost Model
model = XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    objective='reg:squarederror'
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)


# Accuracy
score = r2_score(y_test, predictions)

print(f"Model Accuracy (R2 Score): {score:.2f}")

# Save model
joblib.dump(model, "models/milk_yield_model.pkl")



from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_test, predictions)

print(f"Mean Absolute Error: {mae:.2f} litres")
print("Model saved successfully!")
