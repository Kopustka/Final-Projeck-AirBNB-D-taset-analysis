import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, MeanShift, AffinityPropagation, SpectralClustering, DBSCAN, OPTICS, \
    AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from scipy.stats import zscore


def z_score(df, column, vis):
    """
    Detects outliers in a given numerical column using the Z-score method.
    Outliers are identified as data points with Z-scores beyond the threshold (default: |Z| > 3).
    Optionally visualizes the distribution of data and detected outliers.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the column to analyze.
    column (str): The name of the numerical column to check for outliers.
    vis (bool): Whether to visualize the outlier detection process.

    Returns:
    pd.DataFrame: The DataFrame with detected outliers removed.
    """
    # Extract numerical data from the specified column, dropping NaN values
    data = df[column].dropna().values

    # Compute the mean and standard deviation
    mean = np.mean(data)
    std_dev = np.std(data)

    # Calculate Z-scores for each data point
    z_scores = (data - mean) / std_dev

    # Define the threshold for outlier detection
    threshold = 3
    outliers = np.where(np.abs(z_scores) > threshold)  # Identify indices of outliers

    if vis:
        # Visualization of data points and detected outliers
        plt.figure(figsize=(10, 6))
        plt.plot(data, 'bo', label='Data')  # Original data points
        plt.plot(outliers[0], data[outliers], 'ro', label='Outliers')  # Outliers marked in red
        plt.axhline(mean, color='g', linestyle='dashed', linewidth=2, label='Mean')
        plt.axhline(mean + threshold * std_dev, color='r', linestyle='dotted', linewidth=2, label='Outlier threshold')
        plt.axhline(mean - threshold * std_dev, color='r', linestyle='dotted', linewidth=2)

        plt.title(f'Outlier Detection ({column}) using Z-Score')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.legend()
        plt.show()

    # Print detected outliers
    print(f"Detected outliers in {column}:", data[outliers])

    # Remove detected outliers from the DataFrame
    df = df[~df[column].isin(data[outliers])]
    return df


def quartile_method(df, column, vis):
    """
    Detects outliers using the Interquartile Range (IQR) method.
    Outliers are defined as values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR.
    Optionally visualizes the data distribution and detected outliers.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the column to analyze.
    column (str): The name of the numerical column to check for outliers.
    vis (bool): Whether to visualize the outlier detection process.

    Returns:
    pd.DataFrame: The DataFrame with detected outliers removed.
    """
    # Extract numerical data from the specified column, dropping NaN values
    data = df[column].dropna().values

    # Compute Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1  # Compute the interquartile range

    # Define the lower and upper bounds for outlier detection
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify outliers
    outliers = np.where((data < lower_bound) | (data > upper_bound))  # Indices of outliers

    if vis:
        # Visualization of data points and detected outliers
        plt.figure(figsize=(10, 6))
        plt.plot(data, 'bo', label='Data')  # Original data points
        plt.plot(outliers[0], data[outliers], 'ro', label='Outliers')  # Outliers marked in red
        plt.axhline(Q1, color='orange', linestyle='dashed', linewidth=2, label='Q1 (25th percentile)')
        plt.axhline(Q3, color='green', linestyle='dashed', linewidth=2, label='Q3 (75th percentile)')
        plt.axhline(lower_bound, color='red', linestyle='dotted', linewidth=2, label='Lower outlier threshold')
        plt.axhline(upper_bound, color='red', linestyle='dotted', linewidth=2, label='Upper outlier threshold')

        plt.title(f'Outlier Detection ({column}) using IQR Method')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.legend()
        plt.show()

    # Print detected outliers count
    print(f"Detected outliers in {column}:", len(data[outliers]))

    # Remove detected outliers from the DataFrame
    df = df[~df[column].isin(data[outliers])]
    return df

