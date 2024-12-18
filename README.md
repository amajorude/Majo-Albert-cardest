# Majo-Albert-cardest
This repository provides implementations of cardinality estimation algorithms for analyzing text files and data streams. The primary objective is to estimate the number of unique elements in large-scale or streaming data efficiently and compare the results with the different techniques. The repository focuses on two main methods: the recordinality algorithm and the HyperLogLog (HLL) algorithm. Additionally, synthetic data streams with Zipfian distributions are generated to evaluate the algorithms' performance under controlled conditions.

The datasets folder contains real-world text files. The algorithms process all text files in this folder to estimate the number of unique words and save the results in corresponding output folders, these being recardinality_results and hyperloglog_results respectively.

In Synthetic_data.py there is the code required to generate the data streams text files created following the Zipfian distribution for diferent values of alpha.

In Recordinality.py we implement the recordinality algorithm to estimate the number of different words in both the real text files as well as the synthetic data streams. It saves in recordinality_results and synthetic_results a csv containing the estimated number of unique words and the error compared to the real number of words for different values of elements to keep k for each text file.

Similarly, in HLL.py we apply the HyperLogLog algorithm to get the same results and save them in hyperloglog_results and synthetic_results.
