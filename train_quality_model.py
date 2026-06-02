import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("datasets/milk_quality.csv")

# Remove spaces in column names
df.columns = df.columns.str.strip()

# Encode categorical columns
label_encoders = {}

for col in df.select_dtypes(include=["object", "string"]).columns:

    le = LabelEncoder()

    df[col] = le.fit_transform(df[col].astype(str))

    label_encoders[col] = le

# Features and target
X = df.drop("Grade", axis=1)
y = df["Grade"]

# Feature Scaling
scaler = StandardScaler()

X = scaler.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train SVM Model
model = SVC(
    kernel='linear',
    C=0.5,
    gamma='scale'
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print(f"Model Accuracy: {accuracy:.2f}")

# Save model
joblib.dump(model, "models/milk_quality_model.pkl")

print("Milk Quality Model Saved Successfully!")
print(df["Feed_Quantity_kg"].describe())