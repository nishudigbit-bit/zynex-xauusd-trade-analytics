# Zynex XAUUSD Demo Trade Analytics

**Portfolio project by Nishant Keshri**  
**Purpose:** Demonstrate trade-data cleaning, performance analysis, reporting, and documentation for digital-markets / trading-operations roles.

> **Important:** This dataset is from a demo account. It is not evidence of live trading performance or a promise of future results. The account currency is not specified in the export, so P&L figures are shown in the export's unspecified account currency. Closing records can include partial closes; therefore, the record-level positive share below must not be described as a position-level win rate.

## Project goals

- Clean a broker-export CSV and remove its summary/footer row.
- Calculate net P&L consistently as `reported profit + commission + swap`.
- Summarize activity by instrument, side, closing reason, and date.
- Create charts that make the data reviewable.
- Preserve privacy by omitting original broker record IDs from the public dataset.

## Dataset overview

- Source: user-provided Zynex demo-account CSV export.
- Exported closing records included in analysis: **117**
- Date range by opening time: **2026-09-15 to 2026-10-09**
- Instruments: **XAGUSD (4), XAUUSD (113)**
- Original export had repeated IDs associated with partial-close records; this public dataset omits those IDs.

## Summary from the provided export

| Metric | Result |
|---|---:|
| Closing records analysed | 117 |
| Reported profit before commission/swap | 828.88 |
| Commission total | -119.18 |
| Swap total | 0.00 |
| Net P&L (profit + commission + swap) | 709.70 |
| Positive closing records | 70 |
| Negative closing records | 47 |
| Zero-P&L closing records | 0 |
| Positive-record share (not position win rate) | 59.83% |
| Median net P&L per closing record | 4.70 |
| Mean net P&L per closing record | 6.07 |
| Largest positive closing record | 823.65 |
| Largest negative closing record | -651.92 |
| Median record duration | 4.83 minutes |

**Interpretation caveat:** Aggregate results are sensitive to a small number of large positive and negative records. The export also shows stop-loss and stop-out records and missing stop-loss/take-profit values on many records. This project should be used to demonstrate data analysis, not to claim that the trading strategy is proven or consistently profitable.

### Net P&L by instrument

| Instrument | Closing records | Net P&L |
|---|---:|---:|
| XAGUSD | 4 | 53.63 |
| XAUUSD | 113 | 656.07 |

### Net P&L by side

| Side | Closing records | Net P&L |
|---|---:|---:|
| BUY | 59 | -468.84 |
| SELL | 58 | 1178.54 |

### Net P&L by closing reason

| Reason | Closing records | Net P&L |
|---|---:|---:|
| User | 72 | 2110.87 |
| Partial | 10 | 204.72 |
| TP | 7 | 85.97 |
| Stopout | 3 | -767.79 |
| SL | 25 | -924.07 |

## Repository structure

```text
.
├── README.md
├── data/
│   └── demo_closing_records_anonymized.csv
├── src/
│   └── analyze_trades.py
├── charts/
│   ├── daily_net_pnl.png
│   ├── cumulative_net_pnl.png
│   └── net_pnl_by_symbol.png
├── reports/
│   ├── analysis_notes.md
│   ├── by_close_reason.csv
│   ├── by_side.csv
│   ├── by_symbol.csv
│   ├── daily_net_pnl.csv
│   └── summary_metrics.csv
└── requirements.txt
```

## Run locally

```bash
python -m pip install -r requirements.txt
python src/analyze_trades.py
```

## Methodology and limitations

1. The `Total` footer row is excluded by requiring valid open and close timestamps.
2. `net_pnl` is calculated as reported profit + commission + swap.
3. Rows are treated as exported closing records, not necessarily independent trade ideas or positions.
4. Original broker IDs are removed from the public dataset.
5. Account currency, starting balance, equity deposits/withdrawals, and a complete tick/price series are not supplied. Therefore, percentage return, true account-level drawdown, risk-adjusted returns, and strategy expectancy cannot be responsibly inferred from this file alone.
6. Before making performance claims, reconcile this export with the platform's account summary and group partial closes into their underlying positions.

## Future improvements

- Group partial-close records into positions where the platform export provides a reliable parent position/order key.
- Add entry-level planned risk and calculate R-multiples only where initial risk is known.
- Add session/time-of-day analysis after confirming the export timezone.
- Add an annotated TradingView chart case study for selected records.
- Add tests for parsing, net-P&L calculation, and summary totals.

## Disclaimer

This is an educational analytics project based on demo-account data. It is not investment advice, a live-account performance statement, or a recommendation to trade.


## TradingView chart evidence

The `charts/annotated_setups/` folder contains eight owner-supplied TradingView screenshots. The examples show XAUUSD intraday chart analysis, session ranges, support/resistance reactions, liquidity-sweep annotations, and planned risk/reward zones.

[Read the annotated chart case-study guide](reports/annotated_chart_case_studies.md).

**Evidence note:** Chart annotations describe the author's analysis or planned setup. They do not prove that an order was filled or that the annotated risk/reward target was achieved. Realized outcomes must be checked against the trade journal and demo-account export.
