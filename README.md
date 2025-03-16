# Plant Diseases Detection

## Overview
This project provides a web interface for `Plant Diseases Detection` using Flask. It includes backend processing for model loading, image preprocessing, and predictions. The system also allows users to upload images for training and prediction.

## Project Structure

### Backend (`web.py`)
The backend handles model management, image processing, and user interactions.

- **`load_model()`**: Loads the trained `.h5` model file.
- **`preprocessing_image()`**: Scales images to the required dimensions (224x224 or 256x256) for model input.
- **`get_model_description()`**: Provides descriptions for different datasets to help users understand the chosen dataset.
- **`model_page()`**: Manages image selection or user-uploaded images for model prediction.
- **`selected_file()`** and **`upload_file()`**: Handle image display on the webpage.

### Frontend
- **`Home.html`**: The main page containing usage instructions and selection options for the trained models.
- **`Model.html`**: Displays the selected model and allows users to upload images for prediction.
- **`Result.html`**: Shows prediction results after processing an image.

## Cloud Deployment
### 1. Create a Virtual Machine (VM)
1. **Resource Group**: Select the appropriate resource group.
2. **VM Name**: Choose a name for the virtual machine.
3. **Region**: Select `UK-South` (Student subscription available).
4. **Zone**: Choose Zone 1 (Single-zone deployment for simplicity).
5. **Image**: Use Debian (lightweight Linux distribution).
6. **Size**: Select `Standard_D2s_v3` (cost-efficient for small-scale applications).
7. **Authentication**: Use password authentication for ease of access.
8. **Network Configuration**:
   - Enable inbound public access.
   - Default OS disk size: 30GB.
   - Default subnet and network settings.
9. **Deploy**: Finalize and create the VM.

### 2. Connect to the Virtual Machine
1. Navigate to the VM resource in Azure.
2. Click `Connect` and choose SSH.
3. Use Azure CLI for browser-based SSH access.
4. Connect via CLI:
   ```sh
   ssh username@<public-ip>
   ```
   Example:
   ```sh
   ssh dat-fptu@20.90.90.19
   ```

### 3. Set Up the Environment
1. **Ensure Python is installed** (pre-installed on Debian).
2. **Install Git**:
   ```sh
   sudo apt install git
   ```
3. **Clone the Project Repository**:
   ```sh
   git clone <your-repo-url>
   cd <project-folder>
   ```
4. **Set Up Virtual Environment**:
   ```sh
   sudo apt install python3.11-venv
   python3 -m venv venv
   source venv/bin/activate
   ```
5. **Install Required Libraries**:
   ```sh
   pip install -r requirements.txt
   ```
6. **Allow Port 5000 for Public Access**:
   - Go to VM network settings.
   - Add an inbound rule for TCP traffic on port `5000`.

### 4. Run the Application
```sh
python3 app.py
```
The application will be accessible at `http://<public-ip>:5000/`.

## Web Application Flow
1. **Load the Pretrained Model (`.h5` file)**.
2. **Preprocess Images**: Convert input images to the required format.
3. **Model Prediction**: Process user-uploaded images and provide classification results.
4. **Display Results**: Show predictions on the `Result.html` page.