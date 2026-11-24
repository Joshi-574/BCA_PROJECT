import os
import uuid
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import joblib
import numpy as np   # <-- Add this line


# -------------------------
# Flask App
# -------------------------
app = Flask(__name__)
app.secret_key = 'admin'

# -------------------------
# MySQL Connection
# -------------------------
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='Satlite'
)
mycursor = mydb.cursor()

# -------------------------
# Database Functions
# -------------------------
def executionquery(query, values):
    mycursor.execute(query, values)
    mydb.commit()

def retrivequery1(query, values):
    mycursor.execute(query, values)
    return mycursor.fetchall()

def retrivequery2(query):
    mycursor.execute(query)
    return mycursor.fetchall()

# -------------------------
# Routes
# -------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index2')
def index2():
    return render_template("index2.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    message = ''
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']

        if password != c_password:
            message = "Confirm password does not match!"
            return render_template('register.html', message=message)

        # Check if email exists
        query = "SELECT UPPER(email) FROM users"
        email_data = retrivequery2(query)
        email_list = [i[0] for i in email_data]

        if email.upper() in email_list:
            message = "This email ID already exists!"
            return render_template('register.html', message=message)

        # Insert new user (store name too if your DB has 'name' column)
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        executionquery(query, (name, email, password))

        message = "Successfully Registered!"
        return render_template('login.html', message=message)

    return render_template('register.html', message=message)

@app.route('/login', methods=["GET", "POST"])
def login():
    message = ''
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        query = "SELECT UPPER(email) FROM users"
        email_data = retrivequery2(query)
        email_list = [i[0] for i in email_data]

        if email.upper() not in email_list:
            message = "This email ID does not exist!"
            return render_template('login.html', message=message)

        query = "SELECT UPPER(password) FROM users WHERE email = %s"
        password_data = retrivequery1(query, (email,))
        if password.upper() != password_data[0][0]:
            message = "Invalid Password!!"
            return render_template('login.html', message=message)

        # Successful login
        global user_email
        user_email = email
        return redirect('/home')

    return render_template('login.html', message=message)

@app.route('/home')
def home():
    return render_template('uhome.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            return render_template('upload.html', msg="No file part")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', msg="No selected file")
        
        # If file is present, read the CSV
        try:
            df = pd.read_csv(file)
            dataset = df.head(500)  # Show only the first 500 rows
            columns = dataset.columns.values.tolist()  # Get column names
            rows = dataset.values.tolist()  # Get rows as a list of lists
            return render_template('upload.html', columns=columns, rows=rows, msg="Dataset Uploaded Successfully")
        except Exception as e:
            return render_template('upload.html', msg=f"Error: {str(e)}")

    # Render the page with the file upload form
    return render_template('upload.html')

@app.route('/model', methods=['GET', 'POST'])
def model():
    # Static accuracy data for all models
    results = {
        "XGBoost": "93.50%",
        "Random Forest": "93.43%",
        "CNN": "84.90%"
    }

    # Detailed messages for each algorithm
    metrics = {
 
        "xgboost": {
            "name": "XGBoost Classifier",
            "accuracy": 93.50,
            "message": "🚀 XGBoost achieved the highest accuracy (93.50%) on the dataset for disease prediction."
        },
        "random_forest": {
            "name": "Random Forest Classifier",
            "accuracy": 93.43,
            "message": "🌲 Random Forest ensures stable and consistent results with 93.43% accuracy."
        },
        "cnn": {
            "name": "Convolutional Neural Network (CNN)",
            "accuracy": 84.90,
            "message": "🧠 CNN performed with a test accuracy of 84.90%, providing strong results for pattern recognition."
        }
    }

    msg = msg1 = msg2 = ""

    if request.method == "POST":
        algo = request.form.get('algo')

        if algo and algo in metrics:
            model_info = metrics[algo]
            msg = f"✅ Model Selected: {model_info['name']}"
            msg1 = f"📊 Accuracy Achieved: {model_info['accuracy']:.2f}%"
            msg2 = model_info['message']
        else:
            msg = "⚠️ Please select a valid model."

    return render_template('model.html', results=results, msg=msg, msg1=msg1, msg2=msg2)

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        try:
            # 1️⃣ Define expected feature names
            feature_names = [
                'number_of_peak', 'Age', 'Length_of_cycle', 'Estimated_day_of_ovulution',
                'Length_of_Leutal_Phase', 'Length_of_menses', 'Unusual_Bleeding',
                'Height', 'Weight', 'Income', 'BMI', 'Mean_of_length_of_cycle', 'Menses_score'
            ]

            # 2️⃣ Collect user inputs
            features = [float(request.form[name]) for name in feature_names]

            # 3️⃣ Load the trained Random Forest model
            model = joblib.load("RF.joblib")

            # 4️⃣ Prepare input for prediction
            input_array = np.array(features).reshape(1, -1)

            # 5️⃣ Predict class and probability
            rf_pred = model.predict(input_array)
            probabilities = model.predict_proba(input_array)

            # 6️⃣ Map the predicted labels to health states (EXTENDED MAPPING)
            health_mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'D'}

            # Ensure all predicted labels are mapped to a health state
            health_states = [health_mapping[label] for label in rf_pred]

            # Health Suggestions based on the predicted health state
            def get_health_suggestions(health_state):
                if health_state == 'A':
                    return "Maintain a balanced diet, exercise regularly, manage stress effectively."
                elif health_state == 'B':
                    return "Track symptoms, exercise more, eat low-glycemic foods, consult healthcare."
                elif health_state == 'C':
                    return "Seek medical advice, manage weight, monitor hormones, reduce stress."
                elif health_state == 'D':
                    return "Predicted class is outside of A, B, C. Please re-check your model training data target encoding for classes 3 and 4. Consult a medical professional for advice."
                else:
                    return "Unrecognized health state. Consult a medical professional."

            # Format the result
            predicted_class = int(rf_pred[0])
            health_state = health_states[0]
            confidence = round(np.max(probabilities[0]) * 100, 2)

            result = {
                "Predicted_Class": predicted_class,
                "Health_State": health_state,
                "Suggestion": get_health_suggestions(health_state),
                "Confidence": confidence
            }

            # 8️⃣ Send to HTML
            return render_template('prediction.html', predictions=[result])

        except Exception as e:
            return render_template('prediction.html', error=f"Error: {str(e)}")

    return render_template('prediction.html')

if __name__ == "__main__":
    app.run(debug=True)
