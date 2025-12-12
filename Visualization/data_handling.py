# This module comtains a data handling functions for reading CSV files saved from the main notebook.
# It is called in the visualization and slider modules to load data for plotting.
# It also contains a function to extract features from multiple data files for analysis.

# Imports
import csv
import os
import numpy as np

# Function to load data from a CSV file
def load_data(filepath):
    file_path = filepath
    print(f"Reading data from {file_path}")
    with open(file_path, 'r', newline='') as csvfile:
        # Create a DictReader object
        csv_dict_reader = csv.DictReader(csvfile)
        
        t, tau, x, y, z, E, T, IL, s_1_array, s_2_array, Fitness = [], [], [], [], [], [], [], [], [], [], []
        
        for row in csv_dict_reader:
            if row['t'] == '':
                continue  # Skip rows with empty t
            t.append(int(row['t']))
            if row['tau'] == '':
                continue  # Skip rows with empty tau
            tau.append(row['tau'])
            if row['x'] == '':
                continue  # Skip rows with empty x
            x.append(float(row['x']))
            if row['y'] == '':
                continue  # Skip rows with empty y
            y.append(float(row['y']))
            if row['z'] == '':
                continue  # Skip rows with empty z
            z.append(float(row['z']))
            if row['E'] == '':
                continue  # Skip rows with empty E
            E.append(float(row['E']))
            if row['T'] == '':
                continue  # Skip rows with empty T
            T.append(float(row['T']))
            if row['IL'] == '':
                continue  # Skip rows with empty IL
            IL.append(float(row['IL']))
            if row['s_1'] == '':
                continue  # Skip rows with empty s_1
            s_1_array.append(float(row['s_1']))
            if row['s_2'] == '':
                continue  # Skip rows with empty s_2
            s_2_array.append(float(row['s_2']))
            if row['Fitness'] == '':
                continue  # Skip rows with empty Fitness
            Fitness.append(float(row['Fitness']))
    
    return t, tau, x, y, z, E, T, IL, s_1_array, s_2_array, Fitness


# function to extract features from data files
def extract_features(filepath, antigenicity_values):
    import pandas as pd

    amplitudes = []
    c_vals = []
    max_vals1 = []
    max_vals2 = []
    ave_vals1 = []
    ave_vals2 = []
    bifur_c0 = []
    bifur_y0 = []

    # find amplitudes for each file
    for idx, f in enumerate(filepath):
        df = pd.read_csv(f)
        
        y = df["y"].values
        tail = y[-500:]
        center1 = y[500:1000]
        center2 = y[1000:1500]

        amp = tail.max() - tail.min()

        max_val1 = center1.max()
        max_val2 = center2.max()
        ave_val1 = center1.mean()
        ave_val2 = center2.mean()

        # store per run data
        amplitudes.append(amp)
        c_vals.append(antigenicity_values[idx])
        max_vals1.append(max_val1)
        max_vals2.append(max_val2)
        ave_vals1.append(ave_val1)
        ave_vals2.append(ave_val2)

    c_vals = np.array(c_vals)
    amplitudes_0 = np.array(amplitudes)
    max1_non = np.array(max_vals1)
    max2_non =  np.array(max_vals2)
    ave1_non = np.array(ave_vals1)
    ave2_non = np.array(ave_vals2)


    features = np.vstack((c_vals, amplitudes_0, max1_non, max2_non, ave1_non, ave2_non)).T
    return features, c_vals, amplitudes_0

