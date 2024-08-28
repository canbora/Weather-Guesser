import keras
import matplotlib.pyplot as plt
import numpy as np
from keras import layers

image_size = (124, 124)
batch_size = 128
num_classes = 11
epochs = 50

train_ds, val_ds = keras.utils.image_dataset_from_directory(
    "dataset",
    validation_split=0.2,
    subset="both",
    seed=75317531,
    image_size=image_size,
    batch_size=batch_size,
)

model = keras.Sequential(
    [
        layers.Input(shape=(*image_size, 3)),                      # (input)
        layers.RandomFlip("horizontal"),                           # (preprocessing) Randomly flip them
        layers.RandomRotation(0.1),                                # (preprocessing) Randomly rotate them
        layers.Rescaling(1/255),                                   # (preprocessing) Change range from [0, 255] to [0, 1]
        layers.Conv2D(16, kernel_size=(3, 3), activation="relu"),  # convolution layer
        layers.Conv2D(16, kernel_size=(3, 3), activation="relu"),  # convolution layer
        layers.MaxPooling2D(pool_size=(2, 2)),                     # 2x2 max pooling layer
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),  # convolution layer
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),  # convolution layer
        layers.MaxPooling2D(pool_size=(2, 2)),                     # 2x2 max pooling layer
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),  # convolution layer
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),  # convolution layer
        layers.MaxPooling2D(pool_size=(3, 3)),                     # 3x3 max pooling layer
        layers.Conv2D(128, kernel_size=(3, 3), activation="relu"), # convolution layer
        layers.Conv2D(128, kernel_size=(3, 3), activation="relu"), # convolution layer
        layers.GlobalMaxPooling2D(),                               # global max pooling layer (should be 4x4 for 124x124 inputs)
        layers.Dropout(0.3),                                       # (training only) ignore some outputs in last layer
        layers.Dense(num_classes, activation="softmax"),           # fully connected layer followed by softmax
    ]
)

print(model.summary())

callbacks = [
    keras.callbacks.ModelCheckpoint("model.keras", save_best_only=True, verbose=1),
]

model.compile(
    optimizer=keras.optimizers.Adam(3e-4),
    loss=keras.losses.SparseCategoricalCrossentropy(),             # Sparse categorical == one output variable with an integer value for each category
    metrics=[
        keras.metrics.SparseCategoricalAccuracy(name="acc"),
    ],
)

model.fit(
    train_ds,
    epochs=epochs,
    callbacks=callbacks,
    validation_data=val_ds,
    verbose=2
)
