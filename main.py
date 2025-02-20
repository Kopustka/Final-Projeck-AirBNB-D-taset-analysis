import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler

from moduls import show_table
from moduls import z_score, quartile_method
from moduls import preprocessing, time_preprocessing, df_incoding
from moduls import (cluster_data, plot_clusters,
                    evaluate_clusters, kmeans_c,affinity_c,
                    mean_shift_c, spectral_c, dbscan_c,
                    optics_c, agglomerative_c, ansamble_c)
from moduls import k_neighbors
from moduls import importing


dataset_name = "mysarahmadbhat/airbnb-listings-reviews"
download_path = '../data/'

def main():
    importing(dataset_name, download_path)


    file_path = '../data/Airbnb Data/Listings.csv'
    df = pd.read_csv(file_path, encoding="utf-8", encoding_errors="replace", low_memory=False)

    print(('EDA'))
    print(df.info())
    print(df.describe())


    print('Preprocessing \n')
    df = preprocessing(df)
    df = df[['latitude','longitude', 'city', 'district']]

    df_incoding(df)

    for i in df.columns:
        df = z_score(df, i, vis=False)

    for i in df.columns:
        df = quartile_method(df, i, vis=False)


    missing_values = df.isnull().sum()
    print(missing_values)

    print('Clusterization')

    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    kmeans_c(df_scaled)
    k_neighbors(df)
    dbscan_c(df_scaled)
    affinity_c(df_scaled)
    mean_shift_c(df_scaled)
    spectral_c(df_scaled)
    optics_c(df_scaled)

    ansamble_c(df, df_scaled, n_clusters=4)



if __name__ == "__main__":
    main()

