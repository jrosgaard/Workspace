# This module comtains a data handling functions for reading CSV files saved from the main notebook.
# It is called in the visualization and slider modules to load data for plotting.

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