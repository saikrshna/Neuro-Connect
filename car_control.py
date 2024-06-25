import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import joblib
import time
import serial
import requests

# Load the trained classifier model
clf = joblib.load('./random_forest_model.pkl')

# Configure the serial port
ser = serial.Serial('COM9', 115200, timeout=1)  # Adjust the port as necessary

NUM_CHANNELS = 2
BYTES_PER_SAMPLE = 2  # 2 bytes per sample (assuming Arduino sends 10-bit ADC data)

# IP address for sending requests
REQUEST_IP = '172.20.10.6'

# Variables for tracking state duration
current_state = None
start_time = time.time()

try:
    while True:
        # Read and process data from Arduino
        data = ser.read(NUM_CHANNELS * BYTES_PER_SAMPLE)
        if len(data) == NUM_CHANNELS * BYTES_PER_SAMPLE:
            samples = [int.from_bytes(data[i:i+2], byteorder='big') for i in range(0, len(data), 2)]
            print(samples)  
            # Prepare data for prediction
            new_data = pd.DataFrame({'channel1': [samples[0]], 'channel2': [samples[1]]})  
            # Predict the state (calm or tensed) using the trained model
            state = clf.predict(new_data)
            
            if state != current_state:
                # State changed, reset timer
                current_state = state
                start_time = time.time()
            
            # Check if it's time to send request based on state and duration
            if current_state == 'calm' and time.time() - start_time >= 5:  # Send request after 5 seconds of calm state
                requests.get(f'http://{REQUEST_IP}/0')
                print("Sent request to turn off")
                start_time = time.time()  # Reset timer
            elif current_state == 'tensed': 
                requests.get(f'http://{REQUEST_IP}/1')
                print("Sent request to turn on")
                start_time = time.time()  # Reset timer
            
            
        else:
            print("Incomplete data received:", data)
        
        # Delay for 1 second
        time.sleep(1)

except KeyboardInterrupt:
    # Close serial port when interrupted
    ser.close()
