"""
Analyze anonymized Zynex demo-account closing records.
Run from repository root: python src/analyze_trades.py
Net P&L = reported_profit + commission + swap.
The exported rows may include partial closes; record-level statistics are not position-level trade statistics.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "demo_closing_records_anonymized.csv"
OUT = ROOT / "reports"
CHARTS = ROOT / "charts"
OUT.mkdir(exist_ok=True)
CHARTS.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["open_time", "close_time"])
df["net_pnl"] = df["reported_profit"] + df["commission"] + df["swap"]
df = df.sort_values("close_time")
n = len(df)
summary = {
    "closing_records": n,
    "date_start": str(df["open_time"].min()),
    "date_end": str(df["open_time"].max()),
    "gross_reported_profit": round(df["reported_profit"].sum(), 2),
    "commissions": round(df["commission"].sum(), 2),
    "swap": round(df["swap"].sum(), 2),
    "net_pnl": round(df["net_pnl"].sum(), 2),
    "positive_records": int((df["net_pnl"] > 0).sum()),
    "negative_records": int((df["net_pnl"] < 0).sum()),
    "zero_records": int((df["net_pnl"] == 0).sum()),
    "positive_record_share_pct": round((df["net_pnl"] > 0).mean() * 100, 2),
    "median_record_net_pnl": round(df["net_pnl"].median(), 2),
    "mean_record_net_pnl": round(df["net_pnl"].mean(), 2),
    "largest_positive_record": round(df["net_pnl"].max(), 2),
    "largest_negative_record": round(df["net_pnl"].min(), 2),
}
pd.Series(summary).to_csv(OUT / "summary_metrics.csv", header=["value"])
df.groupby(df["close_time"].dt.date)["net_pnl"].sum().to_csv(OUT / "daily_net_pnl.csv")
df.groupby("symbol")["net_pnl"].agg(["count", "sum", "mean"]).to_csv(OUT / "by_symbol.csv")
df.groupby("side")["net_pnl"].agg(["count", "sum", "mean"]).to_csv(OUT / "by_side.csv")
df.groupby("close_reason")["net_pnl"].agg(["count", "sum", "mean"]).to_csv(OUT / "by_close_reason.csv")

daily = df.groupby(df["close_time"].dt.date)["net_pnl"].sum()
plt.figure(figsize=(10, 4.8))
daily.plot(kind="bar")
plt.title("Daily Net P&L — Demo Account")
plt.xlabel("Close date")
plt.ylabel("Net P&L (account currency not specified)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(CHARTS / "daily_net_pnl.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 4.8))
df["net_pnl"].cumsum().plot()
plt.title("Cumulative Net P&L by Closing Record — Demo Account")
plt.xlabel("Closing record in chronological order")
plt.ylabel("Cumulative net P&L (account currency not specified)")
plt.tight_layout()
plt.savefig(CHARTS / "cumulative_net_pnl.png", dpi=160)
plt.close()

print(pd.Series(summary).to_string())
print("\\nReminder: these are closing-record metrics, not independent-position metrics.")
