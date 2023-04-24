import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


def read_file(file_name: str) -> pd.DataFrame:
    """ 
    This function reads the csv file and returns a pandas dataframe.
    Args:
        file_name (str): The name of the file to be read.
    Returns:
        data (pd.DataFrame): The pandas dataframe.
    """
    data = pd.read_csv(file_name)
    data['place'] = file_name.split('_')[4:].pop(0).lower()
    return data


def haversine_distance(lat1: float, lon1: float, lat2: float,
                       lon2: float) -> float:
    """
    This function calculates the distance between two points in miles, using the haversine formula.
    Args:
        lat1 (float): The latitude of the first point.
        lon1 (float): The longitude of the first point.
        lat2 (float): The latitude of the second point.
        lon2 (float): The longitude of the second point.
    Returns:
        res (float): The distance between the two points.
    """
    r = 3959.87433  # In miles. For km use 6372.8 km

    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)

    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)

    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * \
        np.cos(phi2) * np.sin(delta_lambda / 2)**2
    res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))

    return np.round(res, 2)


def remove_outliers(df: pd.DataFrame, col: str, q1: float,
                    q3: float) -> pd.DataFrame:
    """
    This function removes the outliers from a dataframe.
    Args:
        df (pd.DataFrame): The dataframe to be cleaned.
        col (str): The column to be cleaned.
    Returns:
        df (pd.DataFrame): The cleaned dataframe.
    """
    Q1 = df[col].quantile(q1)
    Q3 = df[col].quantile(q3)
    IQR = Q3 - Q1

    df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]

    return df


def optimal_clusters_sse(data: pd.DataFrame, max_k: int,
                         min_percent: float) -> dict:
    """
    This function finds the optimal number of clusters for a dataset based on a minimum percentage per cluster.
    Args:
        data (pd.DataFrame): The dataset to be used.
        max_k (int): The maximum number of clusters to be tested.
        min_percent (float): The minimum percentage of data points that a cluster must contain.
    Returns:
        sse (dict): The sum of squared errors for each number of clusters.
    """
    sse = {}
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, max_iter=1000).fit(data)
        data["clusters"] = kmeans.labels_
        cluster_counts = data["clusters"].value_counts(normalize=True)
        if any(cluster_counts < min_percent):
            break
        sse[k] = kmeans.inertia_  # Inertia: Sum of distances of samples to their closest cluster center
    return sse


def get_customer_types(data: pd.DataFrame, n_clusters: int) -> pd.DataFrame:
    """
    This function returns the customer types for a dataset.
    Args:
        data (pd.DataFrame): The dataset to be used.
        n_clusters (int): The number of clusters to be used.
    Returns:
        customer_types (pd.DataFrame): The customer types.
    """
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42)
    y_kmeans = kmeans.fit_predict(data)

    # Showing the common values for each cluster
    customer_types = pd.DataFrame(kmeans.cluster_centers_,
                                  columns=data.columns)

    # Assigning labels to each cluster
    customer_types['label'] = [
        'customer_type_{}'.format(i + 1) for i in range(n_clusters)
    ]

    # Droping the columns that are not needed
    customer_types.drop(['clusters'], axis=1, inplace=True)

    # Counting number of customers in each cluster
    customer_types['customer_pct'] = [
        round((y_kmeans == i).sum() / len(y_kmeans) * 100, 1)
        for i in range(n_clusters)
    ]

    return customer_types
