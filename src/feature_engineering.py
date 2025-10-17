import pandas as pd
import numpy as np

def make_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create returns, volatility, and VIX change features."""
    df = df.copy()
    df["ret_1d"] = df["SPY_Close"].pct_change()
    df["ret_20d"] = df["SPY_Close"].pct_change(20)
    df["volatility_20d"] = df["ret_1d"].rolling(20).std() * np.sqrt(252)
    df["vix_change_20d"] = df["VIX_Close"].pct_change(20)
    df = df.dropna()
    return df

if __name__ == "__main__":
    from data_loader import load_market_data
    data = load_market_data()
    feats = make_features(data)
    print(feats.head())