import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import joblib
import time
import serial
import pyautogui

# Load the trained classifier model
clf = joblib.load('./random_forest_model.pkl')

# Configure the serial port
ser = serial.Serial('COM9', 115200, timeout=1)  # Adjust the port as necessary

NUM_CHANNELS = 2
BYTES_PER_SAMPLE = 2  # 2 bytes per sample (assuming Arduino sends 10-bit ADC data)

try:
    while True:
        # Read and process data from Arduino
        data = ser.read(NUM_CHANNELS * BYTES_PER_SAMPLE)
        if len(data) == NUM_CHANNELS * BYTES_PER_SAMPLE:
            samples = [int.from_bytes(data[i:i+2], byteorder='big') for i in range(0, len(data), 2)]
            print(samples)  
            #Prepare data for prediction
            new_data = pd.DataFrame({'channel1': [samples[0]], 'channel2': [samples[1]]})  
            # Predict the state (calm or tensed) using the trained model
            state = clf.predict(new_data)
            if(state=='calm'):
                pyautogui.moveRel(0, 10, duration=0.5)
            else:
                pyautogui.moveRel(0, -10, duration=0.5)

            
        else:
            print("Incomplete data received:", data)
        
        # Delay for 1 second
        time.sleep(1)

except KeyboardInterrupt:
    # Close serial port when interrupted
    ser.close()