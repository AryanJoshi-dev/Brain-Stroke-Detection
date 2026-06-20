# Innovations in Stroke Identification — A Machine Learning-Based Diagnostic Model Using Neuroimaging

A Flask web application that uses a deep learning model to detect stroke from brain scan images (CT/MRI).

## Features

- User registration and login system
- Upload brain scan images for stroke detection
- Deep learning model (CNN) classifies images as **Normal** or **Stroke Detected**
- Clean, responsive web interface

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the Model File

The trained model file (`final_model.h5`) is not included in the repository due to its large size.

**Download it separately** and place it in the project root directory (same folder as `app.py`).

### 5. Run the Application

```bash
python app.py
```

The app will start at `http://127.0.0.1:5000/`

## Project Structure

```
stroke model/
├── app.py                 # Main Flask application
├── final_model.h5         # Trained model (not in repo - add manually)
├── requirements.txt       # Python dependencies
├── static/
│   └── style.css          # Custom styles
├── templates/
│   ├── base.html          # Base template with navbar
│   ├── index.html         # Landing page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── home.html          # Home page with project info
│   └── predictions.html   # Upload & prediction page
└── README.md
```

## Tech Stack

- **Backend**: Flask (Python)
- **ML Model**: TensorFlow/Keras (CNN)
- **Image Processing**: OpenCV
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5
