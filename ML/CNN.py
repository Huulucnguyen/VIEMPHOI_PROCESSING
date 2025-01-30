import tensorflow as tf
import numpy as np
from PIL import Image
class CNNClassifier:
    def __init__(self):
        path_to_artifacts = "C:/Users/p0tabe/"
        self.model = tf.keras.models.load_model(path_to_artifacts+'model.h5')
    def predict(self,input_image_url):
        class_names = ['NORMAL', 'PNEUMONIA']
        image = tf.keras.preprocessing.image.load_img(input_image_url)
        img = image.resize((160,160))
        input_arr = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(input_arr, 0)
        predictions = self.model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        status = class_names[np.argmax(score)]
        accuracy = 100 * np.max(score)
        return {"status":status,"accuracy":accuracy}
       # 'D:\\endpoints\\media\\PatientXray\\IM-0003-0001.jpeg'