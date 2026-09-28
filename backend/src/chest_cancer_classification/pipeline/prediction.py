import tensorflow as tf


class PredictionPipeline:
    def __init__(self, model_path: str):
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, input_data):
        predictions = self.model.predict(input_data)
        return predictions