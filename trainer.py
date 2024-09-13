#!/usr/bin/env python3
import keras
import matplotlib.pyplot as plt
import numpy as np
from keras import layers
import keras_tuner
import os.path

image_size = (124, 124)
batch_size = 128
num_classes = 11
epochs = 50


def create_model(hp):
    # First hyperparams should be between 12-24
    # Last hyperparams should be between 96-192
    hyperparams = [hp.Int(f"conv{i}", min_value=12*2**(i//2), max_value=24*2**(i//2), step=2*2**(i//2)) for i in range(8)]
    model = keras.Sequential(
        [
            layers.Input(shape=(*image_size, 3)),                                   # (input)
            layers.RandomFlip("horizontal"),                                        # (preprocessing) Randomly flip them
            layers.RandomRotation(0.1),                                             # (preprocessing) Randomly rotate them
            layers.Rescaling(1/255),                                                # (preprocessing) Change range from [0, 255] to [0, 1]
            layers.Conv2D(hyperparams[0], kernel_size=(3, 3), activation="relu"),   # convolution layer
            layers.Conv2D(hyperparams[1], kernel_size=(3, 3), activation="relu"),   # convolution layer
            layers.MaxPooling2D(pool_size=(2, 2)),                                  # 2x2 max pooling layer
            layers.Conv2D(hyperparams[2], kernel_size=(3, 3), activation="relu"),   # convolution layer
            layers.Conv2D(hyperparams[3], kernel_size=(3, 3), activation="relu"),   # convolution layer
            layers.MaxPooling2D(pool_size=(2, 2)),                                  # 2x2 max pooling layer
            layers.Conv2D(hyperparams[4], kernel_size=(3, 3), activation="relu"),   # convolution layer
            layers.Conv2D(hyperparams[5], kernel_size=(3, 3), activation="relu"),   # convolution layer
            layers.MaxPooling2D(pool_size=(3, 3)),                                  # 3x3 max pooling layer
            layers.Conv2D(hyperparams[6], kernel_size=(3, 3), activation="relu"),   # convolution layer
            layers.Conv2D(hyperparams[7], kernel_size=(3, 3), activation="relu"),   # convolution layer
            layers.GlobalMaxPooling2D(),                                            # global max pooling layer (should be 4x4 for 124x124 inputs)
            layers.Dropout(hp.Float("dropout", min_value=0, max_value=0.6)),        # (training only) ignore some outputs in last layer
            layers.Dense(num_classes, activation="softmax"),                        # fully connected layer followed by softmax
        ]
    )

    model.compile(
        optimizer=keras.optimizers.Adam(hp.Float("rate", min_value=1e-4, max_value=1e-2, sampling="log")),
        loss=keras.losses.SparseCategoricalCrossentropy(),             # Sparse categorical == one output variable with an integer value for each category
        metrics=[
            keras.metrics.SparseCategoricalAccuracy(name="acc"),
        ],
    )

    return model


def train_model(tune_again=False):

    model = None
    if not tune_again:
        try:
            model = keras.saving.load_model("tuned_model.keras")
        except ValueError: # no tuned model file
            pass

    if model is None: # Need to tune model first

        train_ds, val_ds = keras.utils.image_dataset_from_directory(
            "dataset",
            validation_split=0.2,
            subset="both",
            seed=75317531,
            image_size=image_size,
            batch_size=batch_size,
        )

        # First, tune the hyperparameters
        tuner = keras_tuner.Hyperband(
            hypermodel=create_model,
            objective="val_loss",
            max_epochs=9,
            overwrite=True,
            directory="hypertuning",
            project_name="weather",
        )
        print(tuner.search_space_summary())

        tuner.search(
            train_ds,
            epochs=1,
            validation_data=val_ds,
            verbose=2
        )

        # Recreate the model with the best hyperparameters
        model = create_model(tuner.get_best_hyperparameters(1)[0])

        print(model.summary())

        model.save("tuned_model.keras", overwrite=True)

    # now train it

    callbacks = [
        keras.callbacks.ModelCheckpoint("trained_model.keras", save_best_only=True, verbose=1),
    ]

    model.fit(
        train_ds,
        epochs=epochs,
        callbacks=callbacks,
        validation_data=val_ds,
        verbose=2
    )
    return model

if __name__ == '__main__':
    train_model()