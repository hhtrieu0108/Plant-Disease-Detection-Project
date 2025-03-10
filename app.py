from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import io

app = Flask(__name__)

# Load all models
models = {
    "model1": load_model("models/model1.h5"),
    "model2": load_model("models/model2.h5"),
    "model3": load_model("models/model3.h5"),
    "model5": load_model("models/model4.h5"),
}

def preprocess_image(image):
    image = image.resize((256, 256))  # Adjust based on your model input size
    image = np.array(image) / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

def get_prediction_label(prediction):
    class_labels = ["01Orange___Haunglongbing_(Citrus_greening)",
                            "02Apple___Apple_scab",
                                "03Apple___Black_rot",
                        "04Apple___Cedar_apple_rust",
                                "05Apple___healthy",
                            "06Blueberry___healthy",
                "07Cherry_(including_sour)___healthy",
        "08Cherry_(including_sour)___Powdery_mildew",
"09Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
                    "10Corn_(maize)___Common_rust_",
                        "11Corn_(maize)___healthy",
            "12Corn_(maize)___Northern_Leaf_Blight",
                                "13Grape___Black_rot",
                    "14Grape___Esca_(Black_Measles)",
                                "15Grape___healthy",
    "16Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
                        "17Peach___Bacterial_spot",
                                "18Peach___healthy",
                    "19Pepper,_bell___Bacterial_spot",
                        "20Pepper,_bell___healthy",
                            "21Potato___Early_blight",
                                "22Potato___healthy",
                            "23Potato___Late_blight",
                            "24Raspberry___healthy",
                                "25Soybean___healthy",
                        "26Squash___Powdery_mildew",
                            "27Strawberry___healthy",
                        "28Strawberry___Leaf_scorch",
                        "29Tomato___Bacterial_spot",
                            "30Tomato__Early_blight",
                                "31Tomato___healthy",
                            "32Tomato__Late__Blight",
                            "33Tomato___Leaf_Mold",
                    "34Tomato___Septoria_leaf_spot",
    "35Tomato_Spider_mites Two-spotted_spider_mite",
                            "36Tomato___Target_Spot",
                    "37Tomato___Tomato_mosaic_virus",
        "38Tomato___Tomato_Yellow_Leaf_Curl_Virus"
        ]               # Adjust as needed
    return class_labels[np.argmax(prediction)]

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    selected_model = None
    
    if request.method == "POST":
        if "image" not in request.files or "model" not in request.form:
            return render_template("index.html", error="Missing image or model selection")
        
        image_file = request.files["image"]
        selected_model = request.form["model"]
        
        if selected_model not in models:
            return render_template("index.html", error="Invalid model selected")
        
        image = Image.open(io.BytesIO(image_file.read()))
        processed_image = preprocess_image(image)
        model = models[selected_model]
        prediction = model.predict(processed_image)
        prediction = get_prediction_label(prediction)
    
    return render_template("index.html", prediction=prediction, selected_model=selected_model)

if __name__ == "__main__":
    app.run(debug=True)
