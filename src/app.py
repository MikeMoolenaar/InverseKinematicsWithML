import sys
import time
import pandas as pd
import numpy as np
import os
from copy import copy
from os import path
import importlib
import random
from threading import Thread
from blenderhelper import BlenderHelper
from ml import RobotArmNN

# Reload custom modules, if you import your own module above, also
# import the module here (without from) and an importlib.reload(module_name)
import blenderhelper
import ml
importlib.reload(blenderhelper)
importlib.reload(ml)

scriptDir = os.path.dirname(__file__)
if scriptDir.endswith(".blend"):
    scriptDir = os.path.dirname(scriptDir)

class functions:
    modelSavingPath = path.join(scriptDir, "src", "model")
    trainingdataCsvPath = path.join(modelSavingPath, "training_data_random.csv")
    trainingToCsvRuns = 2000
    offsetX3DCursor = -1.3

    @staticmethod
    def trainModel():
        if not os.path.isfile(functions.trainingdataCsvPath):
            print(f"No traning data ({functions.trainingdataCsvPath}) file found")
            return

        print("Training model...")
        nn = RobotArmNN(2, 3, functions.modelSavingPath)
        loss, accuracy = nn.trainModel(functions.trainingdataCsvPath)
        nn.saveModelData()

        print(f"Loss: {loss} accuracy: {round(accuracy*100, 1)}%")
        print("Done, model trained and weights have been saved")

    @staticmethod
    def peformPrediction():
        cursor = copy(BlenderHelper.get3DCursorPosition())
        cursor[0] = cursor[0] + functions.offsetX3DCursor

        nn = RobotArmNN(2, 3, functions.modelSavingPath)
        nn.loadModelData()
        prediction = nn.predict([cursor[0], cursor[2]])
        print(prediction)
        print(cursor)
        BlenderHelper.setObjectRotation('Joint0', (0-prediction[0], 0, 0))
        BlenderHelper.setObjectRotation('Joint1', (0, 0, 0-prediction[1]))
        BlenderHelper.setObjectRotation('Joint2', (0, 0, 0-prediction[2]))

    @staticmethod
    def trainingToCSV():
        def doTraining():
            rows = []
            for i in range(functions.trainingToCsvRuns):
                joint0Deg = random.randint(0, BlenderHelper.maxValueOfRotation)
                joint1Deg = random.randint(0, BlenderHelper.maxValueOfRotation)
                joint2Deg = random.randint(0, BlenderHelper.maxValueOfRotation)

                # Get the x rotation value of joint0 and the z rotation values of the other joints
                # joint0 rotates in the X asxis rather than the Z axis
                BlenderHelper.setObjectRotation('Joint0', (0-joint0Deg, 0, 0))
                BlenderHelper.setObjectRotation('Joint1', (0, 0, 0-joint1Deg))
                BlenderHelper.setObjectRotation('Joint2', (0, 0, 0-joint2Deg))

                time.sleep(.3)

                ballX, ballY, ballZ = BlenderHelper.getObjectLocation('CenterBall')

                row = [ballX, ballZ, joint0Deg, joint1Deg, joint2Deg]
                rows.append(row)
                print(f"{i}/{functions.trainingToCsvRuns} {row}")

            df = pd.DataFrame(np.array(rows), columns=['ballx', 'ballz', 'joint0', 'joint1', 'joint2'])
            df.to_csv(functions.trainingdataCsvPath, sep='\t', encoding='utf-8', index=False)
            print("Done, values written to CSV")

        t = Thread(target=doTraining)
        t.start()

functionDict = {
    'Random training and export to CSV': functions.trainingToCSV,
    'Train model using existing CSV': functions.trainModel,
    'Move robot to point': functions.peformPrediction
}

# Option can be defined in the blender script
if not 'option' in locals() or option == -1:
    sys.stdout.write('\n======MENU======\n[0=Quit] ')
    x = 1
    for value in functionDict.keys():
        sys.stdout.write(f' [{x}={value}]')
        x+=1

    sys.stdout.flush()

    option = int(input('\nChoose option: '))

if option == 0:
    print("Bye")
else:
    function = list(functionDict.values())[option - 1]
    function()