import numpy as np
import pandas as pd
import os

from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# ==========================================
# 1. SLIDING WINDOW DATA PREPARATION
# ==========================================
# LSTM networks require 3-dimensional data structures for time-series modeling.
# The following functions handle reshaping static samples into rolling historical windows.



def create_sequences(features, target, window_size=24):
    """
    Convert raw time-series data into sequences
    of past `window_size` timesteps.
    """

    X, y = [], []

    for i in range(len(features) - window_size):
        X.append(features[i:(i + window_size)])
        y.append(target[i + window_size])

    return np.array(X), np.array(y)


def generate_and_prepare_data():
    """
    Generates simulated time-series data
    and prepares it for LSTM training
    """

    print("Generating simulated time-series data...")

    np.random.seed(42)

    n_samples = 5000
    time = np.arange(n_samples)

    # Simulated meteorological signals
    temperature = (
        25
        + 5 * np.sin(2 * np.pi * time / 24)
        + np.random.normal(0, 1, n_samples)
    )

    humidity = (
        60
        + 15 * np.cos(2 * np.pi * time / 24)
        + np.random.normal(0, 2, n_samples)
    )

    wind_speed = np.abs(
        15
        + 5 * np.sin(2 * np.pi * time / 12)
        + np.random.normal(0, 2, n_samples)
    )

    pressure = np.random.normal(1013, 5, n_samples)

    # Target AQI
    aqi = (
        0.3 * temperature
        + 0.2 * humidity
        + 0.1 * wind_speed
        + np.random.normal(0, 5, n_samples)
    )

    # Normalize AQI to 1–5
    aqi = np.clip(
        1 + (aqi - aqi.min()) / (aqi.max() - aqi.min()) * 4,
        1,
        5
    )

    features = np.column_stack(
        (temperature, humidity, wind_speed, pressure)
    )

    # Sliding window
    window_size = 24

    X, y = create_sequences(
        features,
        aqi,
        window_size
    )

    print(f"Raw data shape: {features.shape}")
    print(f"Sequence Shape (X): {X.shape}")
    print(f"Target Shape (y): {y.shape}")

    # Chronological split
    split_idx = int(len(X) * 0.8)

    X_train = X[:split_idx]
    X_test = X[split_idx:]

    y_train = y[:split_idx]
    y_test = y[split_idx:]

    print("Training Shape:", X_train.shape)
    print("Testing Shape:", X_test.shape)

    return X_train, X_test, y_train, y_test


# ==========================================
# 2. LIGHTER LSTM MODEL
# ==========================================

def build_lstm_model(input_shape):
    """
    Lightweight LSTM architecture
    optimized for laptop training
    """

    model = Sequential([

        # Smaller LSTM
        LSTM(
            32,
            activation='tanh',
            return_sequences=True,
            input_shape=input_shape
        ),

        Dropout(0.2),

        # Second smaller LSTM
        LSTM(
            16,
            activation='tanh'
        ),

        Dense(1)

    ])

    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )

    return model


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":

    os.makedirs('models', exist_ok=True)

    # Load Data
    X_train, X_test, y_train, y_test = generate_and_prepare_data()

    # Build Model
    model = build_lstm_model(
        input_shape=(
            X_train.shape[1],
            X_train.shape[2]
        )
    )

    model.summary()

    # ==========================================
    # 3. TRAINING CONFIGURATION
    # ==========================================

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True,
        verbose=1
    )

    print("\nStarting Offline LSTM Training...")

    history = model.fit(

        X_train,
        y_train,

        epochs=10,              # Reduced from 50
        batch_size=64,          # Increased speed
        validation_split=0.1,   # Reduced load
        shuffle=False,          # Important for time-series

        callbacks=[early_stopping],

        verbose=1
    )

    # ==========================================
    # 4. SAVE MODEL
    # ==========================================

    model_path = "models/lstm_model.h5"

    model.save(model_path)

    print(f"\nModel saved to '{model_path}'")

    # ==========================================
    # 5. EVALUATE MODEL
    # ==========================================

    loss, mae = model.evaluate(
        X_test,
        y_test,
        verbose=0
    )

    print(f"\nFinal Test Set Evaluation")
    print(f"MSE: {loss:.4f}")
    print(f"MAE: {mae:.4f}")