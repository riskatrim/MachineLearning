# -*- coding: utf-8 -*-
"""rockpaperscissors-ML Pemula-Riska Tri Mardilah.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QQVUMcgBco6nHC8foH3qdQP94cS_X554
"""

# Name : Riska Tri Mardilah
# username : chikayyz
# email : rchika532@gmail.com
# No Hp : +6282285366786
# Alamat : Jl. Veteran Gang Pemuda No.97B, Kabupaten Lahat, Sumatera Selatan

import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator

!wget --no-check-certificate \
  https://dicodingacademy.blob.core.windows.net/picodiploma/ml_pemula_academy/rockpaperscissors.zip\
  -O /tmp/rockpaperscissors.zip

import zipfile,os
local_zip = '/tmp/rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()

base_dir = '/tmp/rockpaperscissors/rps-cv-images'

os.listdir('/tmp/rockpaperscissors/rps-cv-images')

train_rock_dir = os.path.join(train_dir, 'rock')
train_paper_dir = os.path.join(train_dir, 'paper')
train_scissors_dir = os.path.join(train_dir, 'scissors')

validation_rock_dir = os.path.join(validation_dir, 'rock')
validation_paper_dir = os.path.join(validation_dir, 'paper')

from sklearn.model_selection import train_test_split

train_rock_dir = train_test_split(os.listdir('/tmp/rockpaperscissors/hasil_split/train/rock'), test_size = 0.40)
validation_rock_dir = train_test_split(os.listdir('/tmp/rockpaperscissors/hasil_split/val/rock'), test_size = 0.40)
train_paper_dir = train_test_split(os.listdir('/tmp/rockpaperscissors/hasil_split/train/paper'), test_size = 0.40)
validation_paper_dir = train_test_split(os.listdir('/tmp/rockpaperscissors/hasil_split/val/paper'), test_size = 0.40)
train_scissors_dir = train_test_split(os.listdir('/tmp/rockpaperscissors/hasil_split/train/scissors'), test_size = 0.40)
validation_scissors_dir = train_test_split(os.listdir('/tmp/rockpaperscissors/hasil_split/val/scissors'), test_size = 0.40)

datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,
                    horizontal_flip=True,
                    shear_range = 0.2,
                    validation_split=0.4,
                    fill_mode = 'nearest')

train_generator = datagen.flow_from_directory(
        base_dir,
        subset="training",
        target_size=(150, 150),
        batch_size=4,
        class_mode='categorical')
 
validation_generator = datagen.flow_from_directory(
        base_dir,
        subset="validation",
        target_size=(150, 150),
        batch_size=4,
        class_mode='categorical')

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(loss='categorical_crossentropy',
              optimizer=tf.optimizers.Adam(),
              metrics=['accuracy'])
model.summary()

model.fit(
      train_generator,
      steps_per_epoch=45,
      epochs=100,
      validation_data=validation_generator,
      validation_steps=3,
      verbose=2)

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
 
uploaded = files.upload()
 
for fn in uploaded.keys():
 
  # predicting images
  path = fn
  img = image.load_img(path, target_size = (150,150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis = 0)
 
  images = np.vstack([x])
  classes = model.predict(images, batch_size=10)
  
  print(fn)
  if classes[0][0] == 1:
    print('paper')
  elif classes[0][1] == 1:
    print('rock')
  elif classes[0][2] == 1:
    print('scissors')
  else:
    print('invalid image')