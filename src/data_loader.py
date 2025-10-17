import yfinance as yf
import pandas as pd

def load_market_data(start="2004-01-01", end=None):
    """Download SPY and VIX data from Yahoo Finance."""
    data = yf.download(["SPY", "^VIX"], start=start, end=end, progress=False)
    
    # Fix for new yfinance format — it now returns single-level columns
    if isinstance(data.columns, pd.MultiIndex):
        data = data["Close"]  # pick close prices if multi-indexed
    
    # Rename columns
    data = data.rename(columns={"SPY": "SPY_Close", "^VIX": "VIX_Close"})
    
    # Keep only these columns
    df = data[["SPY_Close", "VIX_Close"]]
    return df

if __name__ == "__main__":
    df = load_market_data()
    print(df.head())
