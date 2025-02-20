import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

def preprocessing(df):
    max_size = 50000
    # Сокращение выборки случайным образом (например, до 5000 записей)
    df = df.sample(n=max_size, random_state=42) if len(df) > max_size else df

    # Удаляем пропущенные значения
    df = df.dropna()

    return df

def time_preprocessing(df):
    """
    Converts the 'host_since' column to a datetime format and extracts time-based features.

    This function:
    - Converts 'host_since' to datetime format.
    - Extracts 'Year', 'Month', 'Day', and 'Hour' features.
    - Removes the original 'host_since' column.

    Parameters:
        df (pd.DataFrame): The input dataset.

    Returns:
        pd.DataFrame: The dataset with new time-related features.
    """
    print("Formatting time data...\n")
    df["host_since"] = pd.to_datetime(df["host_since"], errors='coerce', utc=True)  # Convert to datetime

    # Check for conversion errors (NaT values)
    print(f"Missing values in 'host_since': {df['host_since'].isna().sum()}")

    # Extract relevant date-time features
    df["Year"] = df["host_since"].dt.year
    df["Month"] = df["host_since"].dt.month
    df["Day"] = df["host_since"].dt.day
    df["Hour"] = df["host_since"].dt.hour

    df = df.drop(columns=["host_since"])  # Remove the original column

    return df

def df_incoding(df):
    # Вывод информации о данных перед обработкой
    print("До обработки:")
    print(df.info())
    print(df.head())

    # Заполнение пропущенных значений
    for column in df.columns:
        if df[column].dtype == "object":
            df[column].fillna("Unknown", inplace=True)  # Заполняем строки "Unknown"
        else:
            df[column].fillna(df[column].median(), inplace=True)  # Заполняем числа медианой

    # Преобразование категориальных признаков в числовые
    label_enc = LabelEncoder()
    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = label_enc.fit_transform(df[column])  # Кодируем строки в числа

    # Масштабирование данных
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    # Преобразуем обратно в DataFrame для удобства
    df = pd.DataFrame(df_scaled, columns=df.columns)

    print(df.info())

    return df