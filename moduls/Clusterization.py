import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, MeanShift, AffinityPropagation, SpectralClustering, DBSCAN, OPTICS, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import numpy as np
from scipy.stats import mode

def cluster_data(model, name, df_scaled):
    clusters = model.fit_predict(df_scaled)
    return clusters

# Функция для визуализации кластеров
def plot_clusters(clusters, name, df_scaled):
    pca = PCA(n_components=2)
    df_pca = pca.fit_transform(df_scaled)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df_pca[:, 0], y=df_pca[:, 1], hue=clusters, palette="viridis", alpha=0.7)
    plt.title(f"Метод: {name}")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.legend(title="Кластеры")
    plt.show()

# Функция оценки качества кластеризации
def evaluate_clusters(data, clusters, name):
    if len(set(clusters)) > 1:  # Проверка на корректное число кластеров
        silhouette = silhouette_score(data, clusters)
        davies_bouldin = davies_bouldin_score(data, clusters)
        calinski_harabasz = calinski_harabasz_score(data, clusters)

        print(f"{name}:")
        print(f"  Silhouette Score: {silhouette:.4f} (чем выше, тем лучше)")
        print(f"  Davies-Bouldin Score: {davies_bouldin:.4f} (чем ниже, тем лучше)")
        print(f"  Calinski Harabasz: {calinski_harabasz:.4f}")
        print("-" * 50)
    else:
        print(f"{name}: Недостаточно кластеров для оценки.")
        print("-" * 50)

def kmeans_c(df_scaled):
    # 1️⃣ K-Means (Метод K-средних)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10, init='k-means++')
    clusters_kmeans = cluster_data(kmeans, "K-Means", df_scaled)
    plot_clusters(clusters_kmeans, "K-Means", df_scaled)
    evaluate_clusters(df_scaled, clusters_kmeans, "K-Means")

def affinity_c(df_scaled):
    # 2️⃣ Affinity Propagation
    affinity = AffinityPropagation(random_state=42,preference=-50, damping=0.75, max_iter=500)
    clusters_affinity = cluster_data(affinity, "Affinity Propagation", df_scaled)
    plot_clusters(clusters_affinity, "Affinity Propagation", df_scaled)
    evaluate_clusters(df_scaled, clusters_affinity, "Affinity Propagation")

def mean_shift_c(df_scaled):
    # 3️⃣ Mean Shift
    mean_shift = MeanShift(bandwidth=1.0)
    clusters_mean_shift = cluster_data(mean_shift, "Mean Shift", df_scaled)
    plot_clusters(clusters_mean_shift, "Mean Shift", df_scaled)
    evaluate_clusters(df_scaled, clusters_mean_shift, "Mean Shift")

def spectral_c(df_scaled):
    # 4️⃣ Spectral Clustering
    spectral = SpectralClustering(n_clusters=4, random_state=42, assign_labels='discretize')
    clusters_spectral = cluster_data(spectral, "Spectral Clustering", df_scaled)
    plot_clusters(clusters_spectral, "Spectral Clustering", df_scaled)
    evaluate_clusters(df_scaled, clusters_spectral, "Spectral Clustering")

def dbscan_c(df_scaled):
    # 5️⃣ DBSCAN
    dbscan = DBSCAN(eps=0.65, min_samples=8, metric='euclidean')
    clusters_dbscan = cluster_data(dbscan, "DBSCAN", df_scaled)
    plot_clusters(clusters_dbscan, "DBSCAN", df_scaled)
    evaluate_clusters(df_scaled, clusters_dbscan, "DBSCAN")

def optics_c(df_scaled):
    # 6️⃣ OPTICS
    optics = OPTICS(min_samples=5,xi=0.05)
    clusters_optics = cluster_data(optics, "OPTICS", df_scaled)
    plot_clusters(clusters_optics, "OPTICS", df_scaled)
    evaluate_clusters(df_scaled, clusters_optics, "OPTICS")

def agglomerative_c(df_scaled):
    # 7️⃣ Agglomerative Clustering (Иерархическая кластеризация)
    agglomerative = AgglomerativeClustering(n_clusters=4)
    clusters_agglomerative = cluster_data(agglomerative, "Agglomerative Clustering", df_scaled)
    plot_clusters(clusters_agglomerative, "Agglomerative Clustering", df_scaled)
    evaluate_clusters(df_scaled, clusters_agglomerative, "Agglomerative Clustering")


def ansamble_c(df, df_scaled, n_clusters):
    # Запуск разных методов кластеризации
    models = {
        'KMeans': KMeans(n_clusters=n_clusters, random_state=42, n_init=10, init='k-means++'),
        'DBSCAN': DBSCAN(eps=0.65, min_samples=8, metric='euclidean'),
        'MeanShift': MeanShift(bandwidth=1.0),
        'AffinityPropagation': AffinityPropagation(random_state=42,preference=-50, damping=0.75, max_iter=500),
        'Agglomerative': AgglomerativeClustering(n_clusters=n_clusters, linkage='ward'),
        'Spectral': SpectralClustering(n_clusters=4, random_state=42, assign_labels='discretize')
    }

    cluster_results = {}
    for name, model in models.items():
        labels = model.fit_predict(df_scaled)
        cluster_results[name] = labels

    # Ансамбль: объединение кластеров (мажоритарное голосование)
    ensemble_labels = np.array(list(cluster_results.values()))
    final_labels = np.apply_along_axis(lambda x: mode(x)[0], axis=0, arr=ensemble_labels)

    df['Cluster'] = final_labels

    # Визуализация кластеров
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df['longitude'], y=df['latitude'], hue=df['Cluster'], palette='tab10')
    plt.title('Ансамблевая кластеризация')
    plt.xlabel('Долгота')
    plt.ylabel('Широта')
    plt.legend(title='Кластер')
    plt.show()

    # Оценка качества кластеризации
    silhouette = silhouette_score(df_scaled, final_labels)
    print(f'Silhouette Score ансамблевого метода: {silhouette:.4f}')

    return df