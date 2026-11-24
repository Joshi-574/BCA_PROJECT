# PCOD Disease Prediction Using Machine Learning

## Project Overview

PCOD Disease Prediction Using Machine Learning is a web-based application designed to predict the risk of Polycystic Ovarian Disease (PCOD) using machine learning techniques.

The project aims to assist in identifying potential PCOD risk based on relevant health-related input data. It combines a machine learning model with a user-friendly web interface to provide prediction results.

## Objectives

- To develop a machine learning-based PCOD prediction system.
- To analyze health-related data for identifying potential PCOD risk.
- To integrate a trained Random Forest model into a web application.
- To provide a simple and user-friendly interface for entering details and viewing predictions.
- To demonstrate the practical application of machine learning in healthcare.

## Technologies Used

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

### Backend
- Python
- Flask

### Machine Learning
- Random Forest Classifier
- Scikit-learn
- Pandas
- NumPy
- Joblib

### Development Tools
- Jupyter Notebook
- Visual Studio Code
- Git and GitHub

## Project Structure

```text
PCOD/
│
└── CODE/
    ├── BACKEND/
    │   ├── MAIN.IPYNB
    │   ├── PCOD.csv
    │   ├── RF.joblib
    │   └── x_train.csv
    │
    └── FRONTEND/
        ├── app.py
        ├── db.sql
        ├── RF.joblib
        │
        ├── static/
        │   ├── assets/
        │   │   ├── css/
        │   │   ├── fonts/
        │   │   ├── images/
        │   │   └── js/
        │   └── vendor/
        │
        └── templates/
            ├── about.html
            ├── index.html
            ├── login.html
            ├── model.html
            ├── prediction.html
            ├── register.html
            ├── upload.html
            └── ...
```

## Machine Learning Model

The project uses a Random Forest Classifier for PCOD risk prediction.

The model is trained using the available dataset and saved as a `.joblib` file for integration with the Flask application.

## Application Workflow

1. User opens the PCOD web application.
2. User registers or logs into the application.
3. User provides the required input information.
4. The Flask backend processes the submitted information.
5. The trained Random Forest model performs prediction.
6. The application displays the prediction result.

## Installation and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/Joshi-574/BCA_PROJECT.git
```

### 2. Navigate to the Frontend Folder

```bash
cd BCA_PROJECT/CODE/FRONTEND
```

### 3. Install Required Libraries

```bash
pip install flask pandas numpy scikit-learn joblib
```

### 4. Run the Application

```bash
python app.py
```

### 5. Open in Browser

```text
http://127.0.0.1:5000/
```

Note: Ensure Python and the required dependencies are installed. The trained model file must be available at the path expected by the application. Database configuration may also be required depending on the application setup.

## Project Limitations

- Prediction performance depends on the quality and availability of the dataset.
- Machine learning predictions are not a substitute for professional medical diagnosis.
- Results should be interpreted as preliminary risk indicators.

## Future Enhancements

- Integration with larger and more diverse datasets.
- Comparison of multiple machine learning algorithms.
- Improved prediction performance and model validation.
- Enhanced user interface and reporting features.
- Secure user data management.

## Repository

GitHub: https://github.com/Joshi-574/BCA_PROJECT

## Disclaimer

This project is developed for academic and educational purposes. It is not intended to replace professional medical advice, diagnosis, or treatment.

## Author

**Janga Joshitha**

BCA Final Year Project

