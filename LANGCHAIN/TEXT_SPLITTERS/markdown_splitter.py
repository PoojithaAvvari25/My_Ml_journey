from langchain_text_splitters import RecursiveCharacterTextSplitter,Language
from langchain_community.document_loaders import PyPDFLoader


text = """🤖 Handwritten Digit Recognition — ML Web App
A production-ready Machine Learning web application for recognizing handwritten digits using a CNN (Convolutional Neural Network) trained on the MNIST dataset. Features real-time prediction, batch processing, and an interactive handwriting calculator powered by TensorFlow/Keras.

🎯 Machine Learning Features
Deep Learning Model: Custom CNN architecture with 98% accuracy on MNIST test set
Real-time Inference: Sub-100ms prediction latency for single digits
Batch Processing: Parallel prediction on multiple images
Confidence Scoring: Probability distribution over 10 classes (0-9)
Adaptive Preprocessing: Smart image normalization and centering
Server-side ML Pipeline: Gaussian blur smoothing, inversion, resizing
Safe Evaluation: AST-based expression parser (no model injection attacks)
🧠 Model Architecture
CNN with 4 Convolutional Layers:

Conv2D(64, 3×3) + ReLU
Conv2D(32, 3×3) + MaxPool + ReLU
Conv2D(16, 3×3) + MaxPool + ReLU
Conv2D(64, 3×3) + MaxPool + ReLU
Flatten → Dense(128) → Dense(10, Softmax)
Performance:

Accuracy: 98%+ on MNIST test set
Parameters: ~150K
Training Time: ~5 minutes (10 epochs)
Inference Speed: <100ms per image
📋 Requirements
Python 3.8+
TensorFlow/Keras
Flask
OpenCV
Pillow
NumPy
🚀 Installation
1. Clone Repository
git clone https://github.com/PoojithaAvvari/Handwritten-Digit-Recognition-DeepLearning-Web-App
cd Handwritten-Digit-Recognition-DeepLearning-Web-App
2. Create Virtual Environment
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Train Model (Optional)
If you don't have trained_model.h5:

python train.py
5. Run Application
python app.py
Open browser and navigate to http://localhost:5000

📁 Project Structure
Handwritten-Digit-Recognition/
├── app.py                    # Flask backend server
├── train.py                  # Model training script
├── load_model.py             # Single image prediction utility
├── tf_cnn.py                 # Legacy training script
├── requirements.txt          # Python dependencies
├── trained_model.h5          # Trained CNN model (not in repo)
├── templates/
│   └── index.html            # Main web UI
├── static/
│   ├── app.js                # Frontend JavaScript
│   └── style.css             # Stylesheet
├── uploads/                  # Uploaded images (not in repo)
└── README.md                 # This file
🏗️ Architecture
Backend (Flask)
Model Loading: Loads pre-trained TensorFlow model
Image Preprocessing: Converts images to 28×28 MNIST format
Prediction Engine: Returns digit + confidence score
Expression Evaluator: Safe AST-based math evaluation
Frontend (HTML/CSS/JavaScript)
Canvas Drawing: Mouse/touch support for handwriting
API Communication: Fetch requests to Flask endpoints
Gallery Management: Browser localStorage persistence
Real-time Updates: Immediate UI feedback
Model
Architecture: CNN with Conv2D, MaxPooling, Dense layers
Training Data: MNIST (70,000 images, 10 classes: 0-9)
Accuracy: ~98% on test set
Input: 28×28 grayscale images
Output: Softmax probability distribution over 10 digits
🎨 Usage Guide
Drawing Mode
Click/drag on canvas to draw digit
Adjust confidence threshold (default: 0.7)
Enable/disable server smoothing
Click Predict to see result
Click Save to Gallery to store drawing
Upload Mode
Select multiple image files
Adjust settings (threshold, smoothing)
Click Predict All for batch processing
Calculator Mode
Draw digit on canvas
Click Add Digit to append prediction
Use operator buttons to build expression
Click Evaluate to calculate result
Example: Draw 5 → Click + → Draw 3 → Click = → Result: 8

🔧 API Endpoints
Method	Endpoint	Description
GET	/	Main UI page
GET	/model_status	Check if model is loaded
POST	/predict_draw	Predict single drawn digit
POST	/predict_files	Batch predict uploaded images
POST	/predict_and_append	Predict and append to calculator
POST	/append_symbol	Add operator to expression
POST	/clear_expression	Reset calculator expression
GET	/get_expression	Retrieve current expression
POST	/evaluate_expression	Calculate math expression
POST	/upload	Handle file uploads
GET	/list_uploads	List uploaded files
DELETE	/delete_file/<filename>	Remove uploaded file
GET	/uploads/<filename>	Serve uploaded file
🔒 Security Features
Safe Expression Evaluation: AST-based parsing prevents code injection
Filename Sanitization: Uses werkzeug.utils.secure_filename()
Path Traversal Prevention: Restricted file access to uploads/ directory
CSRF Token: Flask sessions for state management

"""

splitter=RecursiveCharacterTextSplitter.from_language(
    language = Language.MARKDOWN,
    chunk_size=400,
    chunk_overlap=0
)

chunks = splitter.split_text(text)
for c in chunks:
    print(c)
    print("&&&&&")
