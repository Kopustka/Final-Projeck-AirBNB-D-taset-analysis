from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt

def k_neighbors(df):
    neighbors = NearestNeighbors(n_neighbors=5)
    neighbors_fit = neighbors.fit(df)
    distances, indices = neighbors_fit.kneighbors(df)
    distances = np.sort(distances[:, 4])  # Берем 5-го ближайшего соседа

    plt.plot(distances)
    plt.xlabel("Точки данных")
    plt.ylabel("Расстояние до 5-го соседа")
    plt.title("K-distance plot для выбора eps")
    plt.show()