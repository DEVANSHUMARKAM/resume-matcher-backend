# backend/download_nltk_data.py

import nltk

# Define the local directory to save the data
DOWNLOAD_DIR = "nltk_data"

# Add the local directory to NLTK's data path
nltk.data.path.append(DOWNLOAD_DIR)

# Download the necessary packages to that specific directory
nltk.download("stopwords", download_dir=DOWNLOAD_DIR)
nltk.download("punkt", download_dir=DOWNLOAD_DIR)

print("NLTK data downloaded successfully to the 'nltk_data' directory.")