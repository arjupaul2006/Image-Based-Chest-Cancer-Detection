import PIL
import tensorflow as tf
import numpy as np

from PIL import Image
import numpy as np
from tensorflow.keras.applications.densenet import preprocess_input

class_names = [
    "Lung adenocarcinoma",
    "Large cell carcinoma",
    "No Cancer Detected",
    "Squamous cell carcinoma"
]


class PredictionPipeline:
    def __init__(self, model: tf.keras.Model, image: PIL.Image.Image):
        self.model = model
        self.image = image

    def preprocess(self, input_data):
        # Resize
        image = input_data.resize((460, 460))

        # Convert to NumPy
        image = np.array(image, dtype=np.float32)

        # Add batch dimension
        image = np.expand_dims(image, axis=0)

        # DenseNet preprocessing
        image = preprocess_input(image)

        return image

    def predict(self):
        # Make prediction
        predictions = self.model.predict(self.preprocess(self.image))

        predicted_index = np.argmax(predictions[0])
        predicted_class = class_names[predicted_index]
        confidence = float(predictions[0][predicted_index] * 100)

        return predicted_class, confidence
