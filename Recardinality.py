import hashlib
import re
import heapq
import numpy as np
import pandas as pd  
import os


def hash_function(z):
    """Hash function to map element z to a hash value."""
    return int(hashlib.md5(str(z).encode()).hexdigest(), 16)

def RECORDINALITY(Z, k):
    """Estimate the cardinality of the set Z using the RECORDINALITY algorithm with parameter k."""
    # Step 1: Initialize S with the first k distinct elements based on hash values.
    S = set()
    hash_values = []
    
    # Precompute hash values for the first k distinct elements
    for z in Z:
        h_value = hash_function(z)
        if h_value not in hash_values:
            hash_values.append(h_value)
            S.add(z)
        if len(S) == k:
            break
    
    # Use a heap to efficiently track the minimum hash value element
    min_heap = [(hash_function(z), z) for z in S]  # (hash_value, element) tuples
    heapq.heapify(min_heap)  # Create a min-heap from these tuples

    R = k  # Initial R value is k
    
    # Step 2: Process each element in Z.
    for z in Z:
        y = hash_function(z)

        # Check if the current element should update R.
        if y > min_heap[0][0] and z not in S:
            # Remove the element with the minimum hash value from the heap
            min_element_hash, min_element = heapq.heappop(min_heap)
            S.remove(min_element)  # Remove the element with the minimum hash value
            S.add(z)  # Add the new element z to the set S

            # Add the new element to the heap with its hash value
            heapq.heappush(min_heap, (y, z))

            R += 1  # Increment R
    
    # Step 3: Return the cardinality estimate.
    cardinality_estimate = k * (1 + 1/k) ** (R - k + 1) - 1
    return cardinality_estimate

def actual_unique_words(file_path):
    """Compute the real number of unique words in a file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    words = re.findall(r'\b\w+\b', text)  # Split the text into words
    unique_words = set(words)  # Use a set to get unique words
    return len(unique_words)


def estimate_unique_words(file_path, k):
    """Estimate the number of unique words in a file using the RECORDINALITY algorithm."""
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into words using regular expressions
    words = re.findall(r'\b\w+\b', text)

    # Use the RECORDINALITY function to estimate the number of unique words
    return RECORDINALITY(words, k)

def error_rate_from_counters(m):
    """Calculate the error rate based on the number of counters (m)."""
    return 1.0 / np.sqrt(m)

def run_experiments_rec(file_path):
    """Run multiple experiments to estimate unique words using RECORDINALITY for various k values."""
    # List of values for k (number of elements for RECORDINALITY)
    k_values = [8, 16, 32, 64, 128, 256, 512]
    results = []

    # Get the actual number of unique words in the file for error calculation
    actual_unique = actual_unique_words(file_path)

    # Run experiments for each value of k
    for k in k_values:
        unique_word_estimates = []

        estimate = estimate_unique_words(file_path, k)
        unique_word_estimates.append(estimate)

        # Calculate the estimate and error
        mean_estimate = np.mean(unique_word_estimates)
        error = abs(actual_unique - mean_estimate)
        relative_error = error / actual_unique  # Relative error as a fraction

        # Store results for this k value
        results.append({
            'k': k,
            'estimate number unique words': mean_estimate,
            'real number unique words': actual_unique,
            'error': error,
            'relative error': relative_error
            })

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
    results_df = run_experiments_rec(file_path)
    print(results_df)
    results_df.to_csv(f'recordinality_results/{filename_without_extension}_rec.csv', index=False)


####################################################################################
#ESTIMATE THE NUMBER OF UNIQUE WORDS IN SYNTHETIC DATA STREAMS 

alphas = [0.25, 0.5, 0.75, 1]  # Zipfian parameter

for alpha in alphas:
    file_path = f'zipfian_data_stream_{alpha}.txt'

    results_df = run_experiments_rec(file_path)

    # Print the results for each m
    print(results_df)

    # sSave the results to a CSV file
    results_df.to_csv(f'synthetic_results/rec_results_data_stream_{alpha}.csv', index=False)












