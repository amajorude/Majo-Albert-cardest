import re
import hyperloglog
import math
import pandas as pd  
import os

def error_rate_from_counters(m):
    """Calculate the error rate (epsilon) from the number of counters (m)"""
    return 1.0 / math.sqrt(m)

def actual_unique_words(file_path):
    """Calculate the actual number of unique words in a file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    words = re.findall(r'\b\w+\b', text)  # Split the text into words
    unique_words = set(words)  # Use a set to get unique words
    return len(unique_words)

def estimate_unique_words(file_path, epsilon):
    """Run HyperLogLog and estimate unique words"""
    # Initialize a HyperLogLog instance with the calculated error rate
    hll = hyperloglog.HyperLogLog(epsilon)

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # Split the text into words using regular expressions
    words = re.findall(r'\b\w+\b', text)

    # Add each word to the HyperLogLog instance
    for word in words:
        hll.add(word)

    # Return the estimated number of unique words
    return len(hll)

def run_experiments_hll(file_path):
    """Run HyperLogLog for different files"""
    # List of values for m (counters)
    m = 8
    results = []

    # Get the actual number of unique words in the file for error calculation
    actual_unique = actual_unique_words(file_path)

    # Run experiments for each value of m
    while m <= 512:
        epsilon = error_rate_from_counters(m)
        
        # Run HyperLogLog for a single time (one run)
        estimate = estimate_unique_words(file_path, epsilon)

        # Calculate the error (absolute and relative)
        error = abs(actual_unique - estimate)
        relative_error = error / actual_unique  # Relative error as a fraction

        # Store results for this m value
        results.append({
            'm': m,
            'estimate number unique words': estimate,
            'real number unique words': actual_unique,
            'error': error,
            'relative error': relative_error
        })
        
        m = m * 2  # Double m for the next iteration

    # Create a DataFrame from the results list
    results_df = pd.DataFrame(results)

    # Return the results DataFrame
    return results_df


###################################################################################
# ESTIMATE THE NUMBER OF UNIQUE WORDS IN REAL DATASETS

# Specify the folder path
folder_path = 'datasets'

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    filename_without_extension, _ = os.path.splitext(filename)
    results_df = run_experiments_hll(file_path)
    print(results_df)
    results_df.to_csv(f'hyperloglog_results/{filename_without_extension}_hll.csv', index=False)


####################################################################################
#ESTIMATE THE NUMBER OF UNIQUE WORDS IN SYNTHETIC DATA STREAMS 

alphas = [0.25, 0.5, 0.75, 1]  # Zipfian parameter

for alpha in alphas:
    file_path = f'zipfian_data_stream_{alpha}.txt'

    results_df = run_experiments_hll(file_path)

    # Print the results for each m
    print(results_df)

    # Save the results to a CSV file
    results_df.to_csv(f'synthetic_results/hyperloglog_results_data_stream_{alpha}.csv', index=False)























