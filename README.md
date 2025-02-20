# Проект: Сегментация данных Airbnb

Этот проект предназначен для анализа, предобработки и кластеризации данных Airbnb с целью сегментации объявлений на основе их характеристик. Проект включает в себя загрузку данных, их предобработку, обнаружение аномалий, кластеризацию и визуализацию результатов.

---

## Описание датасета

Датасет содержит информацию об объявлениях Airbnb, включая их местоположение, цены, отзывы и другие характеристики. Основные колонки:


| **Колонка**                   | **Описание**                                  | **Тип данных**      | **Характеристика**                           |
| ----------------------------- | --------------------------------------------- | ------------------- | -------------------------------------------- |
| `listing_id`                  | Уникальный идентификатор объявления           | Числовой (int)      | Категориальный, идентификатор                |
| `name`                        | Название объявления                           | Текст               | Неструктурированные данные                   |
| `host_id`                     | Уникальный ID хоста                           | Числовой (int)      | Категориальный, идентификатор                |
| `host_since`                  | Дата регистрации хоста                        | Дата                | Временной ряд                                |
| `host_location`               | Локация хоста                                 | Текст               | Категориальный, может содержать шум          |
| `host_response_time`          | Время ответа хоста (быстро, редко и т.д.)     | Категориальный      | Может быть пропущенные значения              |
| `host_response_rate`          | Процент ответов хоста                         | Числовой (float, %) | Могут быть пропущенные значения              |
| `host_acceptance_rate`        | Процент одобрения заявок                      | Числовой (float, %) | Отражает активность хоста                    |
| `host_is_superhost`           | Является ли супер-хостом                      | Бинарный (bool)     | 0 или 1                                      |
| `host_total_listings_count`   | Количество объявлений у хоста                 | Числовой (int)      | Может быть аномалии (очень большие значения) |
| `host_has_profile_pic`        | Есть ли фото у хоста                          | Бинарный (bool)     | 0 или 1                                      |
| `host_identity_verified`      | Подтверждена ли личность хоста                | Бинарный (bool)     | 0 или 1                                      |
| `neighbourhood`               | Район объявления                              | Категориальный      | Может содержать ошибки в написании           |
| `district`                    | Округ объявления                              | Категориальный      | Может пересекаться с neighbourhood           |
| `city`                        | Город объявления                              | Категориальный      | Можно использовать для регионального анализа |
| `latitude`                    | Географическая широта                         | Числовой (float)    | Географическая информация                    |
| `longitude`                   | Географическая долгота                        | Числовой (float)    | Географическая информация                    |
| `property_type`               | Тип жилья (квартира, дом и т.д.)              | Категориальный      | Влияет на цену                               |
| `room_type`                   | Тип комнаты (вся квартира, отдельная комната) | Категориальный      | Влияет на цену                               |
| `accommodates`                | Количество гостей                             | Числовой (int)      | Влияет на цену                               |
| `bedrooms`                    | Количество спален                             | Числовой (int)      | Может иметь пропущенные значения             |
| `amenities`                   | Список удобств (WiFi, кухня и т.д.)           | Текстовый список    | Нужно разбивать на бинарные фичи             |
| `price`                       | Цена за ночь                                  | Числовой (float)    | Основной целевой признак                     |
| `minimum_nights`              | Минимальное количество ночей                  | Числовой (int)      | Может содержать выбросы                      |
| `maximum_nights`              | Максимальное количество ночей                 | Числовой (int)      | Возможны аномалии (например, 9999 ночей)     |
| `review_scores_rating`        | Общий рейтинг (из 100)                        | Числовой (float)    | Качественная метрика                         |
| `review_scores_accuracy`      | Оценка точности описания                      | Числовой (float)    | Качественная метрика                         |
| `review_scores_cleanliness`   | Оценка чистоты                                | Числовой (float)    | Качественная метрика                         |
| `review_scores_checkin`       | Оценка заселения                              | Числовой (float)    | Качественная метрика                         |
| `review_scores_communication` | Оценка коммуникации                           | Числовой (float)    | Качественная метрика                         |
| `review_scores_location`      | Оценка расположения                           | Числовой (float)    | Качественная метрика                         |
| `review_scores_value`         | Оценка стоимости/качества                     | Числовой (float)    | Качественная метрика                         |
| `instant_bookable`            | Можно ли моментально забронировать            | Бинарный (bool)     | 0 или 1                                      |

В своем проекте я затронул лишь небольшой объём данных. 
В будущем планируеться добавление сигментации других значений.
---

## Структура проекта

Проект состоит из нескольких модулей, каждый из которых выполняет определённую задачу:

### 1. **importing.py**
Загрузка данных с Kaggle и чтение CSV-файлов.

#### Функции:
- **importing(dataset_name, download_path)**: Загружает датасет с Kaggle и сохраняет его в указанную директорию.
- **csv_reader(path)**: Читает CSV-файл и возвращает DataFrame.

---

### 2. **Preprocesing.py**
Предобработка данных, включая обработку пропущенных значений, кодирование категориальных признаков и масштабирование.

#### Функции:
- **preprocessing(df)**: Удаляет пропущенные значения и сокращает размер выборки (если она слишком большая).
- **time_preprocessing(df)**: Преобразует столбец `host_since` в отдельные признаки (год, месяц, день, час).
- **df_incoding(df)**: Заполняет пропущенные значения, кодирует категориальные признаки и масштабирует данные.

---

### 3. **Anomaly_detection.py**
Обнаружение аномалий в данных с использованием методов Z-score и Interquartile Range (IQR).

#### Функции:
- **z_score(df, column, vis)**: Обнаруживает аномалии с использованием Z-score. Визуализирует результаты, если `vis=True`.
- **quartile_method(df, column, vis)**: Обнаруживает аномалии с использованием IQR. Визуализирует результаты, если `vis=True`.

---

### 4. **Clusterization.py**
Кластеризация данных с использованием различных алгоритмов: K-Means, DBSCAN, Affinity Propagation, Mean Shift, Spectral Clustering, OPTICS, Agglomerative Clustering.

#### Функции:
- **cluster_data(model, name, df_scaled)**: Применяет модель кластеризации к данным.
- **plot_clusters(clusters, name, df_scaled)**: Визуализирует результаты кластеризации с использованием PCA.
- **evaluate_clusters(data, clusters, name)**: Оценивает качество кластеризации с использованием метрик Silhouette Score, Davies-Bouldin Score и Calinski-Harabasz Score.
- **kmeans_c(df_scaled)**: Кластеризация с использованием K-Means.
- **affinity_c(df_scaled)**: Кластеризация с использованием Affinity Propagation.
- **mean_shift_c(df_scaled)**: Кластеризация с использованием Mean Shift.
- **spectral_c(df_scaled)**: Кластеризация с использованием Spectral Clustering.
- **dbscan_c(df_scaled)**: Кластеризация с использованием DBSCAN.
- **optics_c(df_scaled)**: Кластеризация с использованием OPTICS.
- **agglomerative_c(df_scaled)**: Кластеризация с использованием Agglomerative Clustering.
- **ansamble_c(df, df_scaled, n_clusters)**: Ансамблевая кластеризация, объединяющая результаты нескольких методов.

---

### 5. **Table_vis.py**
Визуализация данных в виде таблицы с использованием библиотеки `tkinter`.

#### Функции:
- **show_table(dataframe)**: Отображает DataFrame в виде таблицы с возможностью прокрутки.

---

### 6. **Utils.py**
Вспомогательные функции для анализа данных.

#### Функции:
- **k_neighbors(df)**: Строит K-distance plot для выбора параметра `eps` в DBSCAN.

---

### 7. **main.py**
Основной скрипт, который объединяет все этапы работы: загрузку данных, предобработку, обнаружение аномалий, кластеризацию и визуализацию.

---

## Как использовать проект

1. **Установка зависимостей**:
   Убедитесь, что у вас установлены все необходимые библиотеки:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn tkinter
   ```

2. **Загрузка данных**:
   Загрузите датасет с Kaggle, указав имя датасета и путь для сохранения:
   ```python
   dataset_name = "mysarahmadbhat/airbnb-listings-reviews"
   download_path = '../data/'
   importing(dataset_name, download_path)
   ```

3. **Запуск основного скрипта**:
   Запустите `main.py`, чтобы выполнить все этапы анализа:
   ```bash
   python main.py
   ```

---

### Процесс работы алгоритма в `main.py`

В файле `main.py` реализован полный цикл анализа данных: от загрузки и предобработки до кластеризации и визуализации. Ниже описаны действия, которые выполняются в процессе работы программы, с указанием вызова каждой функции.

---

### 1. **Загрузка данных**
   - **Функция**: `importing(dataset_name, download_path)`
   - **Действие**: Загружает датасет с Kaggle и сохраняет его в указанную директорию.
   - **Код**:
     ```python
     importing(dataset_name, download_path)
     ```

---

### 2. **Чтение данных**
   - **Функция**: `pd.read_csv(file_path, encoding="utf-8", encoding_errors="replace", low_memory=False)`
   - **Действие**: Читает CSV-файл с данными Airbnb и загружает их в DataFrame.
   - **Код**:
     ```python
     file_path = '../data/Airbnb Data/Listings.csv'
     df = pd.read_csv(file_path, encoding="utf-8", encoding_errors="replace", low_memory=False)
     ```

---

### 3. **Exploratory Data Analysis (EDA)**
   - **Функции**: `df.info()`, `df.describe()`
   - **Действие**: Выводит основную информацию о данных (типы колонок, количество строк) и описательную статистику (средние значения, минимумы, максимумы и т.д.).
   - **Код**:
     ```python
     print('EDA')
     print(df.info())
     print(df.describe())
     ```

---

### 4. **Предобработка данных**
   - **Функция**: `preprocessing(df)`
   - **Действие**: Удаляет пропущенные значения и сокращает размер выборки (если она слишком большая).
   - **Также в модуле `preprocessing(df)` можно задать количество элементов, с которыми будет происходить взаимодействие, так как в датасете около 250 тысяч элементов, это поможет ускорить время работы**
   - **Код**:
     ```python
     df = preprocessing(df)
     ```

   - **Функция**: Выбор колонок `df[['latitude', 'longitude', 'city', 'district']]`
   - **Действие**: Оставляет только нужные колонки для дальнейшего анализа.
   - **Код**:
     ```python
     df = df[['latitude', 'longitude', 'city', 'district']]
     ```

   - **Функция**: `df_incoding(df)`
   - **Действие**: Заполняет пропущенные значения, кодирует категориальные признаки и масштабирует данные.
   - **Код**:
     ```python
     df_incoding(df)
     ```

---

### 5. **Обнаружение аномалий**
   - **Функция**: `z_score(df, i, vis=False)`
   - **Действие**: Обнаруживает аномалии в каждом столбце с использованием метода Z-score.
   - **Код**:
     ```python
     for i in df.columns:
         df = z_score(df, i, vis=False)
     ```

   - **Функция**: `quartile_method(df, i, vis=False)`
   - **Действие**: Обнаруживает аномалии в каждом столбце с использованием метода Interquartile Range (IQR).
   - **Код**:
     ```python
     for i in df.columns:
         df = quartile_method(df, i, vis=False)
     ```

---

### 6. **Проверка пропущенных значений**
   - **Функция**: `df.isnull().sum()`
   - **Действие**: Выводит количество пропущенных значений в каждой колонке.
   - **Код**:
     ```python
     missing_values = df.isnull().sum()
     print(missing_values)
     ```

---

### 7. **Масштабирование данных**
   - **Функция**: `StandardScaler()`
   - **Действие**: Масштабирует данные для подготовки к кластеризации.
   - **Код**:
     ```python
     scaler = StandardScaler()
     df_scaled = scaler.fit_transform(df)
     ```

---

### 8. **Кластеризация**
   - **Функция**: `kmeans_c(df_scaled)`
   - **Действие**: Выполняет кластеризацию с использованием алгоритма K-Means.
   - **Код**:
     ```python
     kmeans_c(df_scaled)
     ``![Pasted image 20250220192954](https://github.com/user-attachments/assets/b01ed498-62aa-4301-b4bd-e42f9e5bbde4)
`
![Pasted image 20250220192954](https://github.com/user-attachments/assets/15f97d2d-dfb2-4e13-8710-9744facf729d)
- K-Means:
  - Silhouette Score: 0.5433 (чем выше, тем лучше)
  - Davies-Bouldin Score: 0.6418 (чем ниже, тем лучше)
  - Calinski Harabasz: 3202.3818
  
  - **Функция**: `k_neighbors(df)`
  - **Действие**: Строит K-distance plot для выбора параметра `eps` в DBSCAN.
  - **Код**:
     ```python
     k_neighbors(df)
     ```
![Pasted image 20250220193014](https://github.com/user-attachments/assets/440a75de-c969-4577-bd43-36b39a04abfe)

   - **Функция**: `dbscan_c(df_scaled)`
   - **Действие**: Выполняет кластеризацию с использованием алгоритма DBSCAN.
   - **Код**:
     ```python
     dbscan_c(df_scaled)
     ```
![Pasted image 20250220193026](https://github.com/user-attachments/assets/6a82370c-d111-426d-96c1-23faadacb3bd)
- DBSCAN:
  - Silhouette Score: 0.5157 (чем выше, тем лучше)
  - Davies-Bouldin Score: 0.5946 (чем ниже, тем лучше)
  - Calinski Harabasz: 2404.3744
  - **Функция**: `affinity_c(df_scaled)`
  - **Действие**: Выполняет кластеризацию с использованием алгоритма Affinity Propagation.
  - **Код**:
     ```python
     affinity_c(df_scaled)
     ```
![Pasted image 20250220193128](https://github.com/user-attachments/assets/64ac62b5-6a57-40bf-a4d1-8ceb70745700)
- Affinity Propagation:
  - Silhouette Score: 0.4358 (чем выше, тем лучше)
  - Davies-Bouldin Score: 0.8043 (чем ниже, тем лучше)
  - Calinski Harabasz: 5246.5006
  - **Функция**: `mean_shift_c(df_scaled)`
  - **Действие**: Выполняет кластеризацию с использованием алгоритма Mean Shift.
  - **Код**:
     ```python
     mean_shift_c(df_scaled)
     ```
![Pasted image 20250220193128](https://github.com/user-attachments/assets/b4099557-a277-4892-94a7-088567327cec)
- Mean Shift:
  - Silhouette Score: 0.5393 (чем выше, тем лучше)
  - Davies-Bouldin Score: 0.6407 (чем ниже, тем лучше)
  - Calinski Harabasz: 1531.4642
  - **Функция**: `spectral_c(df_scaled)`
  - **Действие**: Выполняет кластеризацию с использованием алгоритма Spectral Clustering.
  - **Код**:
     ```python
     spectral_c(df_scaled)
     ```
![Pasted image 20250220193225](https://github.com/user-attachments/assets/a7e81bf2-d9ea-45b2-8789-6462c6faf04b)
- Spectral Clustering:
  - Silhouette Score: 0.5433 (чем выше, тем лучше)
  - Davies-Bouldin Score: 0.6420 (чем ниже, тем лучше)
  - Calinski Harabasz: 3202.3334
  - **Функция**: `optics_c(df_scaled)`
  - **Действие**: Выполняет кластеризацию с использованием алгоритма OPTICS.
  - **Код**:
     ```python
     optics_c(df_scaled)
     ```
![Pasted image 20250220191335](https://github.com/user-attachments/assets/8ee8642f-e1e2-4279-b986-0145d6f9bbfd)
- OPTICS:
  - Silhouette Score: -0.0674 (чем выше, тем лучше)
  - Davies-Bouldin Score: 1.1450 (чем ниже, тем лучше)
  - Calinski Harabasz: 18.3809
---

### 9. **Ансамблевая кластеризация**
  - **Функция**: `ansamble_c(df, df_scaled, n_clusters=4)`
  - **Действие**: Объединяет результаты нескольких методов кластеризации с использованием мажоритарного голосования.
  - **Код**:
     ```python
     ansamble_c(df, df_scaled, n_clusters=4)
     ```
![Pasted image 20250220191407](https://github.com/user-attachments/assets/85ad3ead-afc4-40ef-8a7d-01269949ee91)
- Silhouette Score ансамблевого метода: 0.5454
---

### 10. **Завершение работы**
   - **Действие**: Программа завершает выполнение после завершения всех этапов анализа.
   - **Код**:
     ```python
     if __name__ == "__main__":
         main()
     ```

## **Заключение**
  Этот проект представляет собой комплексное решение для анализа и сегментации данных Airbnb. На данном этапе доступно взаимодействие только с Кластеризацией по географическому положению: `['latitude','longitude', 'city', 'district']`
  Но в будущем будут добавлны:
  Кластеризация по ценовым сегментам и типам жилья
  ```
  ['price', 'property_type', 'room_type', 'accommodates', 'review_scores_rating', 'amenities']
```

  Кластеризация по отзывам и рейтингу жилья
  ```
  ['review_scores_rating', 'review_scores_cleanliness', 'review_scores_location', 'review_scores_communication', 'review_scores_value']
  ```

  Сегментация жилья по редким и популярным объектам
  ```
  ['host_total_listings_count', 'host_response_time', 'instant_bookable']
  ```

  Анализ общей структуры данных (иерархическое разбиение на классы) 
  ```
  ['price', 'property_type', 'room_type', 'accommodates', 'minimum_nights', 'maximum_nights']
  ```

  Кластеризация с учетом сложных зависимостей (например, удобства, отзывы, цена) 
  ```
  ['price', 'amenities', 'review_scores_rating', 'host_is_superhost', 'neighbourhood', 'city']
  ```
  
---

