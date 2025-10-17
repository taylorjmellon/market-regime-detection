import pandas as pd
import matplotlib.pyplot as plt
from regime_model import detect_market_regimes
from feature_engineering import make_features
from data_loader import load_market_data


def analyze_regimes(df: pd.DataFrame):
    """Compute statistics for each market regime."""
    stats = df.groupby("regime").agg(
        avg_return=("ret_1d", "mean"),
        volatility=("ret_1d", "std"),
        days=("ret_1d", "count")
    )
    stats["avg_return_%"] = stats["avg_return"] * 100
    stats["volatility_%"] = stats["volatility"] * 100
    return stats


def plot_regime_returns(df: pd.DataFrame, save_path="results/regime_avg_returns.png"):
    """Plot average returns by regime."""
    plt.figure(figsize=(6,4))
    avg_returns = df.groupby("regime")["ret_1d"].mean() * 100
    avg_returns.plot(kind="bar", color=["#4CAF50","#FFC107","#F44336"])
    plt.title("Average Daily Return by Regime")
    plt.ylabel("Return (%)")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"✅ Plot saved to {save_path}")


if __name__ == "__main__":
    # 1. Load and prepare data
    data = load_market_data()
    features = make_features(data)
    df_regimes, model = detect_market_regimes(features, n_regimes=3)

    # 2. Analyze regimes
    stats = analyze_regimes(df_regimes)
    print("\n📊 Regime Statistics:")
    print(stats.round(4))

    # 3. Plot average returns
    plot_regime_returns(df_regimes)
