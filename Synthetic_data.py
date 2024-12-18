import numpy as np

def generate_zipfian_data_stream(n, N, alpha):
    """
    Generate a synthetic data stream of size N following Zipf's law.
    
    Parameters:
    - n: number of distinct elements (x1, x2, ..., xn)
    - N: number of data points in the stream
    - alpha: Zipfian parameter (alpha geq 0)
    
    Returns:
    - data_stream: a list of N elements chosen according to the Zipfian distribution
    """
    # Step 1: Compute the normalization constant c_n
    z = np.array([i**(-alpha) for i in range(1, n+1)])
    c_n = 1 / np.sum(z)

    # Step 2: Compute probabilities for each element x_i
    probabilities = c_n * z

    # Step 3: Generate the data stream by selecting elements based on the probabilities
    data_stream = np.random.choice(range(1, n+1), size=N, p=probabilities)

    return data_stream

def save_data_stream_to_txt(data_stream, filename="data_stream.txt"):
    """
    Save the data stream to a text file.
    
    Parameters:
    - data_stream: The generated synthetic data stream (list or array)
    - filename: The name of the file to save the data stream (default is "data_stream.txt")
    """
    with open(filename, 'w') as f:
        for item in data_stream:
            f.write(f"{item}\n")

# Create data streams for different values of alpha

n = 1000  # Number of distinct elements
N = 10000  # Number of data points in the stream
alphas = [0.25, 0.5, 0.75, 1]  # Zipfian parameter

for alpha in alphas:
    # Generate the data stream
    data_stream = generate_zipfian_data_stream(n, N, alpha)

    # Save the data stream to a text file
    save_data_stream_to_txt(data_stream, f"zipfian_data_stream_{alpha}.txt")

    print("Data stream saved to ", f"zipfian_data_stream_{alpha}.txt")

    # Show the first 10 elements of the generated stream
    print(data_stream[:10])


