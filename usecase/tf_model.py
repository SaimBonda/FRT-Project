import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

def parkinson_predict(image_path):
    np.set_printoptions(suppress=True)
    model = tensorflow.keras.models.load_model('usecase/model.h5', compile=False)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(image_path)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)

    return prediction
