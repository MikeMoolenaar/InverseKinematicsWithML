from datetime import datetime
import os
from os import path
os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # Use CPU

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning) # Ignore FutureWarning's in Tensorflow

from tensorflow import keras
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split

class RobotArmNN:

    xScaler = MinMaxScaler()
    yScaler = MinMaxScaler()

    def __init__(self, numInputs, numOutputs, modelSaveFolder = "./"):
        self.modelSaveFolder = modelSaveFolder
        self.weightsFile = path.join(modelSaveFolder, "model_weights.h5")
        self.scalerXFile = path.join(modelSaveFolder, "xscaler.save")
        self.scalerYFile = path.join(modelSaveFolder, "yscaler.save")
        self.logDir = path.join(modelSaveFolder, "logs", datetime.now().strftime('%Y%m%d-%H%M%S'))

        self.numInputs = numInputs
        self.numOutputs = numOutputs
        self.model = keras.Sequential([
            keras.layers.Dense(50, input_shape=[numInputs], activation='relu'),
            keras.layers.Dense(150, activation='relu'),
            keras.layers.Dense(50, activation='relu'),
            keras.layers.Dense(numOutputs, activation='relu')
        ])

        self.model.compile(loss='mean_squared_error', optimizer='Adam', metrics=['accuracy'])

        # Create a TensorBoard logger
        self.logger = keras.callbacks.TensorBoard(log_dir=self.logDir)

    def trainModel(self, csvFilePath):
        # Import training data
        traningData = pd.read_csv(csvFilePath, delimiter='\t')
        x = traningData.iloc[:, 0:self.numInputs].values  # Get input values of each row
        y = traningData.iloc[:, self.numInputs:self.numInputs + self.numOutputs].values  # Get output values of each row

        # Split up train and test data
        xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.1)

        # Train model
        xTrain = self.xScaler.fit_transform(xTrain)
        yTrain = self.yScaler.fit_transform(yTrain)
        self.model.fit(xTrain, yTrain, epochs=25, shuffle=True, verbose=0, callbacks=[self.logger])

        # Test model
        xTest = self.xScaler.transform(xTest)
        yTest = self.yScaler.transform(yTest)
        loss, accuracy = self.model.evaluate(xTest, yTest, callbacks=[self.logger])

        return loss, accuracy

    def predict(self, inputData):
        inputScaled = self.xScaler.transform([inputData])
        prediction = self.model.predict(np.array(inputScaled))
        outputInverseScaled = self.yScaler.inverse_transform(prediction)
        return outputInverseScaled[0]

    def saveModelData(self):
        if not os.path.exists(self.modelSaveFolder):
            os.makedirs(self.modelSaveFolder)
        joblib.dump(self.xScaler, self.scalerXFile)
        joblib.dump(self.yScaler, self.scalerYFile)
        self.model.save_weights(self.weightsFile)

    def loadModelData(self):
        self.xScaler = joblib.load(self.scalerXFile)
        self.yScaler = joblib.load(self.scalerYFile)
        self.model.load_weights(self.weightsFile)