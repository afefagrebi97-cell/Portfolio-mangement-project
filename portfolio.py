# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 16:50:59 2026

@author: 33749
"""

import pandas as pd

def load_holdings(path="holdings.csv"):
    df = pd.read_csv(path)
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0.0)
    df["avg_buy_price"] = pd.to_numeric(df["avg_buy_price"], errors="coerce").fillna(0.0)
    return df

def get_prices_manual():
    # Change these to today's prices (simple starter mode)
    return {
        "AAPL": 190.0,
        "MSFT": 420.0,
        "TSLA": 230.0,
    }

def compute_portfolio(holdings, prices_dict):
    df = holdings.copy()
    df["current_price"] = df["ticker"].map(prices_dict)

    missing = df[df["current_price"].isna()]["ticker"].tolist()
    if missing:
        print(f"Warning: Missing prices for: {missing}. They will be ignored.")
        df = df.dropna(subset=["current_price"])

    df["market_value"] = df["quantity"] * df["current_price"]
    

    total_value = df["market_value"].sum()

    df["weight_%"] = (df["market_value"] / total_value) * 100 if total_value > 0 else 0.0
    df["pnl"] = (df["current_price"] - df["avg_buy_price"]) * df["quantity"]

    # Handle division by zero for pnl %
    df["pnl_%"] = 0.0
    mask = df["avg_buy_price"] > 0
    df.loc[mask, "pnl_%"] = ((df.loc[mask, "current_price"] / df.loc[mask, "avg_buy_price"]) - 1) * 100

    return df, total_value

def main():
    print("=== Simple Portfolio Tracker (Spyder) ===")

    holdings = load_holdings("holdings.csv")
    prices = get_prices_manual()  # starter mode

    result, total_value = compute_portfolio(holdings, prices)

    pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

    print("\nHoldings breakdown:")
    print(result[["ticker", "quantity", "avg_buy_price", "current_price", "market_value", "weight_%", "pnl", "pnl_%"]])

    print(f"\nTotal portfolio value: {total_value:,.2f}")

if __name__ == "__main__":
    main()



# adding the results in a csv file
   result.to_csv("portfolio_report.csv", index=False)
   print("Saved: portfolio_report.csv")