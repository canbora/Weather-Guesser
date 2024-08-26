## Introduction

This project will consist of a program that, given a photograph, guesses what the weather depicted in the photograph is. It will achieve this using a Convolutional Neural Network.

It currently uses a public domain dataset that can be found in [Kaggle](https://www.kaggle.com/datasets/jehanbhathena/weather-dataset/data).

I am currently preparing this project as part of my internship at Turkcell Communication Services, where I was tasked to implement a program performing image classification.

## Running

- Download the dataset from [Kaggle](https://www.kaggle.com/datasets/jehanbhathena/weather-dataset/data). Put the eleven weather folders in the dataset folder.
- To generate images.npz, which holds normalized image data, run `imageresizer.py`.