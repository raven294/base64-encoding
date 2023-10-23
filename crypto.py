import base64
import os
import logging
from flask import Flask, request, render_template
import hashlib  # Import hashlib for hash calculation

# Logging feature for errors
def logging_file(log_filename):
    # Configure the logging system to write logs to a file
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function for encrypting files and outputting them as base64
def encrypt_file(input_file, output_file):
    try:
        with open(input_file, 'rb') as file:
            file_content = file.read()

        base64_content = base64.b64encode(file_content)

        with open(output_file, 'wb') as encoded_file:
            encoded_file.write(base64_content)

        logging.info(f"Encryption of {input_file} was successful.")
    except FileNotFoundError:
        logging.info(f"File path {input_file} not found.")
    except Exception as a:
        logging.info(f"An error has occurred: {a}")

# Function for calculating the hash of a file
def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            # Read the file in 64 KB chunks
            data = file.read(65536)
            if not data:
                break
            sha256_hash.update(data)
    return sha256_hash.hexdigest()

app = Flask(__name__)

upload_folder = 'upload'
app.config['upload_folder'] = upload_folder

def handle_file_upload(file):
    if not file:
        return "No file provided"
    
    if file.filename == "":
        return "No selected file"
    
    filename = os.path.join(app.config['upload_folder'], file.filename)
    file.save(filename)
    return f"File {file.filename} upload was successful"

@app.route('/')
def index():
    # Render the HTML file for file upload
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    result = handle_file_upload(uploaded_file)
    return result

def main():
    print("This is for encrypting files with base64")

    # Prints the current working directory
    path = os.getcwd()
    print("The current path is:", path)

    log = input("Please choose the location of the logging file: ")
    logging_file(log)

    # Pass a file from a path
    input_path = input("Please choose the file path: ")
    output_path = "base64-encoded.txt"

    encrypt_file(input_path, output_path)

    app.run(debug=True)

if __name__ == "__main__":
    main()
