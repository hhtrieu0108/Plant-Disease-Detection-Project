from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import numpy as np
import tensorflow as tf
from PIL import Image

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load models
def load_model(model_name):
    return tf.keras.models.load_model(f'models/{model_name}.h5')

models = {
    'LeafPDCMD': load_model('MobileNetV2_leaf'),
    'FIELDPLANT': load_model('mobilenet_fieldplant'),
    'XMG4R': load_model('ResNet50_transfer'),
    'PLANTDOC': load_model('Resnet_modifided'),
    'FIELDPLANTVILLAGE': load_model('InceptionV0_PlantVillage_ft')
}

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


SELECTED_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['SELECTED_FOLDER'] = SELECTED_FOLDER


# Check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Preprocess image
def preprocess_image(image_path, target_size=(224, 224)):  
    image = Image.open(image_path).convert("RGB")  
    image = image.resize(target_size)  # Resize to model's required input size  
    image = np.array(image) / 255.0  # Normalize pixel values  
    image = np.expand_dims(image, axis=0)  # Add batch dimension  
    return image

# Home route with model selection
@app.route('/')
def home():
    return render_template('home.html')

# Model route
def get_model_description(model_name):
    descriptions = {
        "LeafPDCMD": """TOTAL IMAGES: 2,571
NUMBER OF CLASSES: 16

CLASS LABELS

DISEASES
1. Early Blight, 5. Molds, 6. Mosaic Virus, 7. Septoria,  8. Bacterial Canker, 
9. Bacterial Spot, 11. Late Blight,  13. Powdery Mildew, 15. Yellow Curl Virus
---------------------------------------------------------
PESTS
0. Aphids, 4. Leafhoppers and Jassids, 10. Flea Beetle,  12. Leafminer, 14. Worm
---------------------------------------------------------
OTHERS
2. Healthy Leaf, 3. Leaf Curl
""",
        "FIELDPLANT": """TOTAL IMAGES: 5,156
NUMBER OF CLASSES: 20

CLASS LABELS

CASSAVA
0. Cassava Bacterial Disease, 1. Cassava Brown Leaf Spot, 2. Cassava Healthy, 3. Cassava Mosaic
---------------------------------------------------------
CORN
4. Corn Blight, 5. Corn Brown Spots, 6. Corn Cercosporiose, 7. Corn Chlorotic Leaf Spot, 8. Corn Healthy, 
9. Corn Insects Damages, 10. Corn Mildiou, 11. Corn Rust, 12. Corn Smut, 13. Corn Streak, 14. Corn Stripe, 15. Corn Yellow Spots, 16. Corn Yellowing
---------------------------------------------------------
TOMATO

17. Tomato Brown Spots, 18. Tomato Mildiou, 19. Tomato Mosaic
""",
    "XMG4R": """TOTAL IMAGES: 3,937
NUMBER OF CLASSES: 8

CLASS LABELS

POTATO
0. Healthy Potato, 2. Unhealthy Potato Early Blight
---------------------------------------------------------
CORN
1. Unhealthy Corn Common Rust
---------------------------------------------------------
TOMATO
3. Unhealthy Tomato Early Blight, 4. Unhealthy Tomato Yellow Leaf Curl Virus, 7. Healthy Tomato
---------------------------------------------------------
APPLE
5. Unhealthy Apple Rust, 6. Unhealthy Apple Scab
""",
    "PLANTDOC": """TOTAL IMAGES: 2,598
NUMBER OF CLASSES: 27

CLASS LABELS

APPLE
0. Apple Scab Leaf, 1. Apple Leaf, 2. Apple Rust Leaf
---------------------------------------------------------
BELL PEPPER
3. Bell Pepper Leaf, 4. Bell Pepper Leaf Spot
---------------------------------------------------------
BLUEBERRY
5. Blueberry Leaf
---------------------------------------------------------
CHERRY
6. Cherry Leaf
---------------------------------------------------------
CORN
7. Corn Gray Leaf Spot, 8. Corn Leaf Blight, 9. Corn Rust Leaf
---------------------------------------------------------
PEACH
10. Peach Leaf
---------------------------------------------------------
POTATO
11. Potato Early Blight, 12. Potato Late Blight
---------------------------------------------------------
RASPBERRY
13. Raspberry Leaf
---------------------------------------------------------
SOYBEAN
14. Soybean Leaf
---------------------------------------------------------
SQUASH
15. Squash Powdery Mildew Leaf
---------------------------------------------------------
STRAWBERRY
16. Strawberry Leaf
---------------------------------------------------------
TOMATO
17. Tomato Early Blight, 18. Tomato Septoria Leaf Spot, 19. Tomato Leaf, 20. Tomato Bacterial Spot, 
21. Tomato Late Blight, 22. Tomato Mosaic Virus, 23. Tomato Yellow Curl Virus, 24. Tomato Mold Leaf
---------------------------------------------------------
GRAPE
25. Grape Leaf, 26. Grape Leaf Black Rot
""",
    "FIELDPLANTVILLAGE": """TOTAL IMAGES: 665
NUMBER OF CLASSES: 38

CLASS LABELS

APPLE
0. Apple - Apple Scab, 1. Apple - Black Rot, 
2. Apple - Cedar Apple Rust, 3. Apple - Healthy
---------------------------------------------------------
BLUEBERRY
4. Blueberry - Healthy
---------------------------------------------------------
CHERRY (INCLUDING SOUR)
5. Cherry - Healthy, 6. Cherry - Powdery Mildew
---------------------------------------------------------
CORN (MAIZE)
7. Corn - Cercospora Leaf Spot (Gray Leaf Spot), 8. Corn - Common Rust, 
9. Corn - Healthy, 10. Corn - Northern Leaf Blight
---------------------------------------------------------
GRAPE
11. Grape - Black Rot, 12. Grape - Esca (Black Measles), 
13. Grape - Healthy, 14. Grape - Leaf Blight (Isariopsis Leaf Spot)
---------------------------------------------------------
PEACH
15. Peach - Bacterial Spot, 16. Peach - Healthy
---------------------------------------------------------
PEPPER (BELL)
17. Pepper (Bell) - Bacterial Spot, 18. Pepper (Bell) - Healthy
---------------------------------------------------------
POTATO
19. Potato - Early Blight, 20. Potato - Healthy, 21. Potato - Late Blight
---------------------------------------------------------
RASPBERRY
22. Raspberry - Healthy
---------------------------------------------------------
SOYBEAN
23. Soybean - Healthy
---------------------------------------------------------
SQUASH
24. Squash - Powdery Mildew
---------------------------------------------------------
STRAWBERRY
25. Strawberry - Healthy, 26. Strawberry - Leaf Scorch
---------------------------------------------------------
TOMATO
27. Tomato - Bacterial Spot, 28. Tomato - Early Blight,  29. Tomato - Healthy, 30. Tomato - Late Blight,  31. Tomato - Leaf Mold, 
32. Tomato - Septoria Leaf Spot, 33. Tomato - Spider Mites (Two-Spotted Spider Mite), 34. Tomato - Target Spot, 35. Tomato - Tomato Mosaic Virus, 36. Tomato - Tomato Yellow Leaf Curl Virus
---------------------------------------------------------
ORANGE
37. Orange - Haunglongbing (Citrus Greening)
"""
    }

    return descriptions.get(model_name, "No description available")


input_sizes = {
    'LeafPDCMD': (224, 224),
    'FIELDPLANT': (256, 256),
    'XMG4R': (256, 256),
    'PLANTDOC': (256, 256),
    'FIELDPLANTVILLAGE': (256, 256)
}

label_dicts = {
    'LeafPDCMD': {
        0: 'Aphids', 1: 'Early Blight', 2: 'Healthy Leaf', 3: 'Leaf Curl', 
        4: 'Leafhoppers and Jassids', 5: 'Molds', 6: 'Mosaic Virus', 7: 'Septoria', 
        8: 'Bacterial Canker', 9: 'Bacterial Spot', 10: 'Flea Beetle', 
        11: 'Late Blight', 12: 'Leafminer', 13: 'Powdery Mildew', 14: 'Worm', 
        15: 'Yellow Curl Virus'
    },
    'PLANTDOC': {
        0: 'Apple Scab Leaf', 1: 'Apple Leaf', 2: 'Apple Rust Leaf', 3: 'Bell Pepper Leaf', 
        4: 'Bell Pepper Leaf Spot', 5: 'Blueberry Leaf', 6: 'Cherry Leaf', 
        7: 'Corn Gray Leaf Spot', 8: 'Corn Leaf Blight', 9: 'Corn Rust Leaf', 
        10: 'Peach Leaf', 11: 'Potato Early Blight', 12: 'Potato Late Blight', 
        13: 'Raspberry Leaf', 14: 'Soybean Leaf', 15: 'Squash Powdery Mildew Leaf', 
        16: 'Strawberry Leaf', 17: 'Tomato Early Blight', 18: 'Tomato Septoria Leaf Spot', 
        19: 'Tomato Leaf', 20: 'Tomato Bacterial Spot', 21: 'Tomato Late Blight', 
        22: 'Tomato Mosaic Virus', 23: 'Tomato Yellow Curl Virus', 24: 'Tomato Mold Leaf', 
        25: 'Grape Leaf', 26: 'Grape Leaf Black Rot'
    },
    'XMG4R': {
        0: 'Healthy Potato', 
        1: 'Unhealthy Corn Common Rust', 
        2: 'Unhealthy Potato Early Blight', 
        3: 'Unhealthy Tomato Early Blight', 
        4: 'Unhealthy Tomato Yellow Leaf Curl Virus', 
        5: 'Unhealthy Apple Rust', 
        6: 'Unhealthy Apple Scab', 
        7: 'Healthy Tomato'
    },
    'FIELDPLANT': {
        0: "Cassava_Bacterial_Disease",
        1: "Cassava_Brown_Leaf_Spot",
        2: "Cassava_Healthy",
        3: "Cassava_Mosaic",
        4: "Corn_Blight",
        5: "Corn_Brown_Spots",
        6: "Corn_Cercosporiose",
        7: "Corn_Chlorotic_Leaf_Spot",
        8: "Corn_Healthy",
        9: "Corn_Insects_Damages",
        10: "Corn_Mildiou",
        11: "Corn_Rust",
        12: "Corn_Smut",
        13: "Corn_Streak",
        14: "Corn_Stripe",
        15: "Corn_Yellow_Spots",
        16: "Corn_Yellowing",
        17: "Tomato_Brown_Spots",
        18: "Tomato_Mildiou",
        19: "Tomato_Mosaic"
    },
    'FIELDPLANTVILLAGE': {
        0: "Orange___Haunglongbing_(Citrus_greening)",
        1: "Apple___Apple_scab",
        2: "Apple___Black_rot",
        3: "Apple___Cedar_apple_rust",
        4: "Apple___healthy",
        5: "Blueberry___healthy",
        6: "Cherry_(including_sour)___healthy",
        7: "Cherry_(including_sour)___Powdery_mildew",
        8: "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        9: "Corn_(maize)___Common_rust_",
        10: "Corn_(maize)___healthy",
        11: "Corn_(maize)___Northern_Leaf_Blight",
        12: "Grape___Black_rot",
        13: "Grape___Esca_(Black_Measles)",
        14: "Grape___healthy",
        15: "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
        16: "Peach___Bacterial_spot",
        17: "Peach___healthy",
        18: "Pepper,_bell___Bacterial_spot",
        19: "Pepper,_bell___healthy",
        20: "Potato___Early_blight",
        21: "Potato___healthy",
        22: "Potato___Late_blight",
        23: "Raspberry___healthy",
        24: "Soybean___healthy",
        25: "Squash___Powdery_mildew",
        26: "Strawberry___healthy",
        27: "Strawberry___Leaf_scorch",
        28: "Tomato___Bacterial_spot",
        29: "Tomato___Early_blight",
        30: "Tomato___healthy",
        31: "Tomato___Late__Blight",
        32: "Tomato___Leaf_Mold",
        33: "Tomato___Septoria_leaf_spot",
        34: "Tomato_Spider_mites Two-spotted_spider_mite",
        35: "Tomato___Target_Spot",
        36: "Tomato___Tomato_mosaic_virus",
        37: "Tomato___Tomato_Yellow_Leaf_Curl_Virus"
    }
}


@app.route('/model/<model_name>', methods=['GET', 'POST'])
def model_page(model_name):
    description = get_model_description(model_name)
    target_size = input_sizes.get(model_name, (224, 224))

    model_image_folder = os.path.join("static", "images", model_name)
    available_images = [f for f in os.listdir(model_image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))] if os.path.exists(model_image_folder) else []

    if request.method == 'POST':
        selected_image = request.form.get('selected_image')

        # If user selects an existing image
        if selected_image:
            image_path = os.path.join(model_image_folder, selected_image)
            
            if not os.path.exists(image_path):
                flash(f'Image "{selected_image}" not found.', 'error')
                return redirect(request.url)

            # Preprocess the image
            image = preprocess_image(image_path, target_size=target_size)
            model = models.get(model_name)

            if model is None:
                flash(f'Model "{model_name}" not found.', 'error')
                return redirect(request.url)

            prediction = model.predict(image)
            result = np.argmax(prediction, axis=1)[0]

            # Get the correct label dictionary for the selected model
            label_dict = label_dicts.get(model_name, {})
            label_name = label_dict.get(result, 'Unknown')

            return render_template(
                'result.html', 
                model_name=model_name, 
                description=description, 
                selected_image=selected_image, 
                result=result, 
                label_name=label_name
            )

        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                flash('No selected file.', 'error')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Preprocess and predict
                image = preprocess_image(file_path, target_size=target_size)
                model = models.get(model_name)

                if model is None:
                    flash(f'Model "{model_name}" not found.', 'error')
                    return redirect(request.url)

                prediction = model.predict(image)
                result = np.argmax(prediction, axis=1)[0]

                # Get the correct label dictionary for the selected model
                label_dict = label_dicts.get(model_name, {})
                label_name = label_dict.get(result, 'Unknown')

                return render_template(
                    'result.html', 
                    model_name=model_name, 
                    description=description, 
                    filename=filename, 
                    result=result, 
                    label_name=label_name
                )

            flash('Invalid file type. Only PNG, JPG, and JPEG are allowed.', 'error')

    return render_template(
        'model.html', 
        model_name=model_name, 
        description=description, 
        available_images=available_images
    )

# Display uploaded image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename))

@app.route('/selected_file/<selected_image>', methods=['GET'])
def selected_file(selected_image):
    # Kiểm tra xem selected_image có giá trị hợp lệ không
    if selected_image:
        return redirect(url_for('static', filename='images/' + selected_image))
    else:
        flash('No image selected.')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
