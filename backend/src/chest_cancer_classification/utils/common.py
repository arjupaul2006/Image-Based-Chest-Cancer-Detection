import os
import sys
from box.exceptions import BoxValueError
from box import ConfigBox
import yaml
from logger import logging
from pathlib import Path
from ensure import ensure_annotations
import json
import pickle
import base64
from exception import CustomeException


@ensure_annotations
def read_yaml_file(file_path: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a ConfigBox object.
    
    Args:
        file_path (str): The path to the YAML file.
        
    Returns:
        ConfigBox: The contents of the YAML file as a ConfigBox object.
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            logging.info(f"YAML file {file_path} read successfully.")
            return ConfigBox(data)
    except BoxValueError as e:
        raise BoxValueError(f"Error in converting YAML file to ConfigBox: {e}")
    except Exception as e:
        raise CustomeException(e, sys)


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logging.info(f"Directory created at: {path}")


@ensure_annotations
def save_json_file(file_path: Path, data: dict):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            logging.info(f"JSON file saved at: {file_path}")
    except Exception as e:
        raise CustomeException(e, sys)


@ensure_annotations
def load_json_file(file_path: Path) -> ConfigBox:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            logging.info(f"JSON file {file_path} loaded successfully.")
            return ConfigBox(data)
    except Exception as e:
        raise CustomeException(e, sys)


@ensure_annotations
def save_binary_file(file_path: Path, data: object):
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
            logging.info(f"Binary file saved at: {file_path}")
    except Exception as e:
        raise CustomeException(e, sys)

@ensure_annotations
def load_binary_file(file_path: Path) -> object:
    try:
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            logging.info(f"Binary file {file_path} loaded successfully.")
            return data
    except Exception as e:
        raise CustomeException(e, sys)

@ensure_annotations
def get_size(path: Path) -> str:
    try:
        size_in_bytes = os.path.getsize(path)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024
    except Exception as e:
        raise CustomeException(e, sys)

@ensure_annotations
def encode_image_to_base64(image_path: Path) -> str:
    """
    Encodes an image file to a base64 string.
    
    Args:
        image_path (Path): The path to the image file.
        
    Returns:
        str: The base64 encoded string of the image.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            logging.info(f"Image at {image_path} encoded to base64 successfully.")
            return encoded_string
    except Exception as e:
        raise CustomeException(e, sys)

@ensure_annotations
def decode_base64_to_image(encoded_string: str, output_path: Path):
    """
    Decodes a base64 string back to an image file.
    
    Args:
        encoded_string (str): The base64 encoded string of the image.
        output_path (Path): The path where the decoded image will be saved.
    """
    try:
        with open(output_path, "wb") as image_file:
            image_file.write(base64.b64decode(encoded_string))
            logging.info(f"Base64 string decoded to image at {output_path} successfully.")
    except Exception as e:
        raise CustomeException(e, sys)