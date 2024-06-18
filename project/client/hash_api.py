import hashlib
import os.path
import pyrebase
from project.consts import *


def calculate_hash(file_path):
    """
    Calculates the MD5 hash of the file at the given path.

    Parameters:
    file_path (str): The path to the file for which the hash is to be calculated.

    Returns:
    str: The MD5 hash of the file, or an empty string if a PermissionError occurs.
    """
    try:
        # Read the file in binary mode and calculate its MD5 hash
        return hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    except PermissionError as e:
        # Print the permission error if it occurs
        print(e)
        return ""


def update_hash_db(hash):
    """
    Updates the local hash database and uploads it to Firebase storage.

    Parameters:
    hash (str): The hash to be added to the hash database.
    """
    # Check if the hash file already exists
    if not os.path.exists(HASHES_FILE_NAME):
        # If the file does not exist, download it from Firebase storage
        storage = download_hash()
    else:
        # Initialize the Firebase app
        firebase = pyrebase.initialize_app(fire_base_config)
        # Get the Firebase storage reference
        storage = firebase.storage()

    # Append the new hash to the local hash file
    with open(HASHES_FILE_NAME, 'a') as hashes_file:
        hashes_file.write(f"\n{hash}")

    # Upload the updated hash file to Firebase storage
    storage.child("virushashes.txt").put(HASHES_FILE_NAME)


def download_hash():
    """
    Downloads the hash database from Firebase storage.

    Returns:
    storage: The Firebase storage reference.
    """
    # Initialize the Firebase app
    firebase = pyrebase.initialize_app(fire_base_config)
    # Get the Firebase storage reference
    storage = firebase.storage()
    # Download the hash file to a specified local directory
    storage.child("virushashes.txt").download(r"D:\update_files", HASHES_FILE_NAME)
    return storage
