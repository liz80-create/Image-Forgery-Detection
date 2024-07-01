import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import PIL 
import cv2
import os
#import itertools
import logging
import matplotlib.pyplot as plt
import json
import sklearn
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from keras.models import Sequential, load_model
from keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout, Activation, GlobalAveragePooling2D
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from PIL import Image, ImageChops, ImageEnhance
from tqdm.notebook import tqdm
class ImageForensics:
    def __init__(self, model_path, class_names):
        self.model = load_model(model_path)
        self.class_names = class_names
        self.image_size = (128, 128)

    def ela_conversion(self, image_path, quality):
        original_image = Image.open(image_path).convert('RGB')
        resaved_file_name = 'resaved_image.jpg'
        original_image.save(resaved_file_name, 'JPEG', quality=quality)
        resaved_image = Image.open(resaved_file_name)
        ela_image = ImageChops.difference(original_image, resaved_image)
        extrema = ela_image.getextrema()
        max_difference = max([pix[1] for pix in extrema])
        ela_image = ImageEnhance.Contrast(ela_image).enhance(60)

        ela_image.save('D:\\RPOOPFINAL\\image_forgery_detection\\forgery_detection\\static\\forgery_detection\\img\\ela_image.jpg')

        return ela_image

    def image_processor(self, image_path):
        ela_image = self.ela_conversion(image_path, 90)
        processed_image = np.array(ela_image.resize(self.image_size)).flatten() / 255.0
        return processed_image.reshape(-1, 128, 128, 3)

    def predict(self, image_path):
        test_image = self.image_processor(image_path)
        y_pred = self.model.predict(test_image)
        y_pred_class = round(y_pred[0][0])
        prediction = self.class_names[y_pred_class]
        confidence = y_pred[0][0] if y_pred_class == 1 else 1 - y_pred[0][0]
        return prediction, confidence * 100

    def display_results(self, image_path):
        original_image = plt.imread(image_path)
        ela_image = self.ela_conversion(image_path, 90)
        fig, ax = plt.subplots(1, 2, figsize=(15, 5))
        ax[0].axis('off')
        ax[0].imshow(original_image)
        ax[0].set_title('Original Image')
        ax[1].axis('off')
        ax[1].imshow(ela_image)
        ax[1].set_title('ELA Image')
        prediction, confidence = self.predict(image_path)
        print(f'Prediction: {prediction}')
        print(f'Confidence: {confidence:0.2f}%')
        print('--------------------------------------------------------------------------------------------------------------')