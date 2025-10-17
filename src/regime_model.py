import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from data_loader import load_market_data
from feature_engineering import make_features


def detect_market_regimes(df: pd.DataFrame, n_regimes: int = 3):
    """Cluster market states into regimes using K-Means."""
    scaler = StandardScaler()
    X = scaler.fit_transform(df[["ret_1d", "volatility_20d", "vix_change_20d"]])
    kmeans = KMeans(n_clusters=n_regimes, n_init=25, random_state=42)
    df["regime"] = kmeans.fit_predict(X)
    return df, kmeans


def plot_regimes(df: pd.DataFrame, save_path: str = "results/regime_plot.png"):
    """Plot SPY price colored by regime and save to file."""
    # ✅ Ensure results/ folder exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    plt.figure(figsize=(12, 6))
    for regime in sorted(df["regime"].unique()):
        sub = df[df["regime"] == regime]
        plt.plot(sub.index, sub["SPY_Close"], label=f"Regime {regime}")

    plt.title("Market Regime Detection via K-Means")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("SPY Price")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"✅ Plot saved to {save_path}")


if __name__ == "__main__":
    # Step 1: Load and prepare data
    data = load_market_data()
    features = make_features(data)

    # Step 2: Detect regimes
    df_regimes, model = detect_market_regimes(features, n_regimes=3)

    # Step 3: Save results
    plot_regimes(df_regimes)

    # Step 4: Print sample output
    print("\n✅ K-Means clustering complete!")
    print(df_regimes[["SPY_Close", "regime"]].head())
        # Step 5: Save regime-labeled data
    output_path = "results/regime_data.csv"
    df_regimes.to_csv(output_path)
    print(f"✅ Data saved to {output_path}")


