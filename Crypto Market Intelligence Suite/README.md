# Crypto Market Intelligence Suite

This project modernizes the original semester notebook into a robust analytics pipeline for **Bitcoin, Ethereum, and Ripple** using CoinGecko market data.

## Business Goals Achieved

1. Compare multi-asset crypto performance on a common timeline.
2. Measure risk and volatility behavior for each asset.
3. Identify peak and trough periods to support timing analysis.
4. Quantify inter-asset dependency through price correlation.
5. Produce reusable outputs (CSV + charts) for reporting and decision support.

## Final Project Highlights

- End-to-end crypto market analytics workflow for Bitcoin, Ethereum, and Ripple.
- Reliable data ingestion from CoinGecko with production-friendly handling.
- Cleaned and aligned time-series dataset ready for analysis.
- Risk and return analytics including annualized and downside volatility.
- Visual reporting package for trends, performance, risk, and correlation.
- Reusable CSV outputs for presentations and future modeling.

## Project Files

- `Crypto Market Intelligence Study.ipynb`: project notebook for exploratory analysis.
- `Crypto Market Intelligence Pipeline.py`: main script to run the complete workflow.
- `cryptodata.csv`: project data artifact.
- `outputs/`: generated after script execution.
  - `market_data_cleaned.csv`
  - `market_data_with_returns.csv`
  - `asset_summary.csv`
  - `price_correlation.csv`
  - `visuals/01_price_trends.png`
  - `visuals/02_indexed_performance.png`
  - `visuals/03_return_boxplot.png`
  - `visuals/04_rolling_volatility.png`
  - `visuals/05_correlation_heatmap.png`

## How To Run

```bash
python "Crypto Market Intelligence Pipeline.py" --days 30 --output-dir outputs
```

Optional arguments:

- `--days`: number of historical days to request from CoinGecko (default: `30`).
- `--output-dir`: destination folder for data tables and visualizations (default: `outputs`).

## Interpretation Notes

- `mean_price` and `median_price` show central tendency of each asset.
- `annualized_volatility` estimates yearly risk from daily returns.
- `downside_volatility` captures only negative-return risk.
- Correlation close to `1` indicates stronger co-movement between assets.

## Suggested Use In Reports

- Use the **indexed performance chart** to compare momentum.
- Use the **rolling volatility chart** to discuss risk regimes.
- Use the **correlation heatmap** to discuss diversification potential.
