import pandas as pd
import serial

# Configure the serial port
ser = serial.Serial('COM3', 115200, timeout=1)  # Adjust the port as necessary

NUM_CHANNELS = 2
BYTES_PER_SAMPLE = 2  # 2 bytes per sample (assuming Arduino sends 10-bit ADC data)

try:
    # Create an empty DataFrame with columns 'channel1' and 'channel2'
    df = pd.DataFrame(columns=['channel1', 'channel2'])
    
    # Main loop to continuously read and record data
    while True:
        # Read data from the serial port
        data = ser.read(NUM_CHANNELS * BYTES_PER_SAMPLE)
        
        # Check if the expected number of bytes is received
        if len(data) == NUM_CHANNELS * BYTES_PER_SAMPLE:
            # Convert bytes to integers and store in a list
            samples = [int.from_bytes(data[i:i+2], byteorder='big') for i in range(0, len(data), 2)]
            
            # Append the samples to the DataFrame
            df = df._append({'channel1': samples[0], 'channel2': samples[1],'state':'tensed'}, ignore_index=True)
            
            # Save the DataFrame to a CSV file
            df.to_csv('./recorded_data2.csv', index=False)
            
            # Print feedback
            print("Data recorded:", samples)
            
        else:
            print("Incomplete data received:", data)
        
except KeyboardInterrupt:
    # Close the serial port when interrupted
    ser.close()
