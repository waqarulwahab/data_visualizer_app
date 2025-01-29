from pathlib import Path

def load_file():
    # Define the data folder path
    data_folder = Path("data")

    # Get a list of all files in the folder
    files = [file for file in data_folder.iterdir() if file.is_file()]

    # Select the first file if files exist
    uploaded_file = files[0] if files else None  # This is a Path object

    return uploaded_file