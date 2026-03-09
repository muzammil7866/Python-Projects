"""
Crypto Market Intelligence Pipeline

A robust implementation of the semester project notebook that:
- Fetches historical market data from CoinGecko for Bitcoin, Ethereum, and Ripple
- Cleans and aligns multi-asset time-series data
- Computes return-based analytics and risk metrics
- Generates business-ready visualizations
- Exports processed datasets and summary tables
"""

from __future__ import annotations

import argparse
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


COINS = ["bitcoin", "ethereum", "ripple"]
VS_CURRENCY = "usd"
BASE_URL = "https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"


@dataclass
class CoinSeries:
    coin_id: str
    dataframe: pd.DataFrame


class CryptoMarketPipeline:
    def __init__(
        self,
        days: int,
        output_dir: Path,
        timeout_seconds: int = 20,
        retries: int = 6,
        retry_backoff: float = 2.0,
        request_spacing_seconds: float = 1.0,
    ) -> None:
        if days <= 0:
            raise ValueError("days must be a positive integer")

        self.days = days
        self.output_dir = output_dir
        self.timeout_seconds = timeout_seconds
        self.retries = retries
        self.retry_backoff = retry_backoff
        self.request_spacing_seconds = request_spacing_seconds

        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "visuals").mkdir(parents=True, exist_ok=True)

        self.raw_series: Dict[str, CoinSeries] = {}
        self.market_data: pd.DataFrame | None = None
        self.price_returns: pd.DataFrame | None = None
        self.summary_table: pd.DataFrame | None = None
        self.correlation_matrix: pd.DataFrame | None = None

    def fetch_all(self, coin_ids: Iterable[str]) -> None:
        coin_id_list = list(coin_ids)
        for idx, coin_id in enumerate(coin_id_list):
            self.raw_series[coin_id] = self._fetch_coin_series(coin_id)
            # Respect public API limits by spacing requests.
            if idx < len(coin_id_list) - 1:
                time.sleep(self.request_spacing_seconds)

    def _fetch_coin_series(self, coin_id: str) -> CoinSeries:
        url = BASE_URL.format(coin_id=coin_id)
        params = {"vs_currency": VS_CURRENCY, "days": self.days}

        last_error = None
        for attempt in range(1, self.retries + 1):
            try:
                response = requests.get(url, params=params, timeout=self.timeout_seconds)
                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    wait_seconds = float(retry_after) if retry_after else self.retry_backoff ** attempt
                    print(f"Rate-limited for {coin_id}. Waiting {wait_seconds:.1f}s before retry.")
                    time.sleep(wait_seconds)
                    continue

                response.raise_for_status()
                payload = response.json()
                return CoinSeries(coin_id=coin_id, dataframe=self._payload_to_frame(coin_id, payload))
            except (requests.RequestException, ValueError) as exc:
                last_error = exc
                if attempt < self.retries:
                    sleep_time = self.retry_backoff ** attempt
                    print(f"Retrying {coin_id} fetch in {sleep_time:.1f}s after error: {exc}")
                    time.sleep(sleep_time)

        raise RuntimeError(f"Unable to fetch data for {coin_id}: {last_error}")

    @staticmethod
    def _payload_to_frame(coin_id: str, payload: dict) -> pd.DataFrame:
        required_keys = ["prices", "market_caps", "total_volumes"]
        for key in required_keys:
            if key not in payload or not payload[key]:
                raise ValueError(f"Payload for {coin_id} is missing '{key}' data")

        df_price = pd.DataFrame(payload["prices"], columns=["timestamp", f"{coin_id}_price"])
        df_cap = pd.DataFrame(payload["market_caps"], columns=["timestamp", f"{coin_id}_market_cap"])
        df_vol = pd.DataFrame(payload["total_volumes"], columns=["timestamp", f"{coin_id}_volume"])

        merged = df_price.merge(df_cap, on="timestamp", how="outer").merge(df_vol, on="timestamp", how="outer")
        merged["timestamp"] = pd.to_datetime(merged["timestamp"], unit="ms", utc=True)
        merged = merged.sort_values("timestamp").drop_duplicates(subset=["timestamp"])

        numeric_cols = [f"{coin_id}_price", f"{coin_id}_market_cap", f"{coin_id}_volume"]
        merged[numeric_cols] = merged[numeric_cols].apply(pd.to_numeric, errors="coerce")
        return merged

    def prepare_market_table(self) -> pd.DataFrame:
        if not self.raw_series:
            raise RuntimeError("No data loaded. Call fetch_all first.")

        merged: pd.DataFrame | None = None
        for coin_id in self.raw_series:
            coin_df = self.raw_series[coin_id].dataframe
            merged = coin_df if merged is None else merged.merge(coin_df, on="timestamp", how="outer")

        if merged is None:
            raise RuntimeError("No coin tables available for merge")

        merged = merged.sort_values("timestamp").reset_index(drop=True)

        numeric_columns = [col for col in merged.columns if col != "timestamp"]
        merged[numeric_columns] = merged[numeric_columns].interpolate(method="linear", limit_direction="both")
        merged[numeric_columns] = merged[numeric_columns].ffill().bfill()

        self.market_data = merged
        return merged

    def compute_returns_and_risk(self) -> pd.DataFrame:
        if self.market_data is None:
            raise RuntimeError("Market data unavailable. Call prepare_market_table first.")

        result = self.market_data.copy()

        price_cols = [f"{coin}_price" for coin in COINS]
        for col in price_cols:
            pct_col = col.replace("_price", "_pct_return")
            log_col = col.replace("_price", "_log_return")
            result[pct_col] = result[col].pct_change()
            result[log_col] = np.log(result[col] / result[col].shift(1))

        return_cols = [c for c in result.columns if c.endswith("_pct_return") or c.endswith("_log_return")]
        result[return_cols] = result[return_cols].replace([np.inf, -np.inf], np.nan).fillna(0.0)

        self.price_returns = result
        return result

    def build_summary(self) -> pd.DataFrame:
        if self.price_returns is None:
            raise RuntimeError("Return table unavailable. Call compute_returns_and_risk first.")

        summary_rows: List[dict] = []
        for coin in COINS:
            price_col = f"{coin}_price"
            ret_col = f"{coin}_pct_return"
            log_col = f"{coin}_log_return"

            idx_max = self.price_returns[price_col].idxmax()
            idx_min = self.price_returns[price_col].idxmin()

            annualized_vol = self.price_returns[ret_col].std() * math.sqrt(365)
            downside = self.price_returns.loc[self.price_returns[ret_col] < 0, ret_col]
            downside_vol = downside.std() * math.sqrt(365) if not downside.empty else 0.0

            summary_rows.append(
                {
                    "coin": coin.title(),
                    "mean_price": self.price_returns[price_col].mean(),
                    "median_price": self.price_returns[price_col].median(),
                    "std_price": self.price_returns[price_col].std(),
                    "annualized_volatility": annualized_vol,
                    "downside_volatility": downside_vol,
                    "max_price": self.price_returns[price_col].max(),
                    "min_price": self.price_returns[price_col].min(),
                    "time_of_max_price": self.price_returns.loc[idx_max, "timestamp"],
                    "time_of_min_price": self.price_returns.loc[idx_min, "timestamp"],
                    "avg_pct_return": self.price_returns[ret_col].mean(),
                    "avg_log_return": self.price_returns[log_col].mean(),
                }
            )

        summary_df = pd.DataFrame(summary_rows)

        price_cols = [f"{coin}_price" for coin in COINS]
        self.correlation_matrix = self.price_returns[price_cols].corr()
        self.summary_table = summary_df
        return summary_df

    def make_visualizations(self) -> None:
        if self.price_returns is None or self.correlation_matrix is None:
            raise RuntimeError("Analysis tables unavailable. Compute summary before plotting.")

        visuals_dir = self.output_dir / "visuals"
        ts = self.price_returns["timestamp"]

        plt.style.use("ggplot")

        # 1) Price history for each coin.
        fig, ax = plt.subplots(figsize=(12, 6))
        for coin in COINS:
            ax.plot(ts, self.price_returns[f"{coin}_price"], label=coin.title())
        ax.set_title("Crypto Prices Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price (USD)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(visuals_dir / "01_price_trends.png", dpi=140)
        plt.close(fig)

        # 2) Indexed performance for apples-to-apples comparison.
        fig, ax = plt.subplots(figsize=(12, 6))
        for coin in COINS:
            indexed = self.price_returns[f"{coin}_price"] / self.price_returns[f"{coin}_price"].iloc[0] * 100
            ax.plot(ts, indexed, label=f"{coin.title()} (Base=100)")
        ax.set_title("Indexed Relative Performance")
        ax.set_xlabel("Time")
        ax.set_ylabel("Indexed Value")
        ax.legend()
        fig.tight_layout()
        fig.savefig(visuals_dir / "02_indexed_performance.png", dpi=140)
        plt.close(fig)

        # 3) Return dispersion.
        fig, ax = plt.subplots(figsize=(10, 6))
        data = [self.price_returns[f"{coin}_pct_return"] for coin in COINS]
        ax.boxplot(data, tick_labels=[coin.title() for coin in COINS], showfliers=False)
        ax.set_title("Daily Percentage Return Distribution")
        ax.set_ylabel("Pct Return")
        fig.tight_layout()
        fig.savefig(visuals_dir / "03_return_boxplot.png", dpi=140)
        plt.close(fig)

        # 4) Rolling volatility trend.
        fig, ax = plt.subplots(figsize=(12, 6))
        for coin in COINS:
            rolling_vol = self.price_returns[f"{coin}_pct_return"].rolling(window=7).std() * math.sqrt(365)
            ax.plot(ts, rolling_vol, label=coin.title())
        ax.set_title("7-Day Rolling Annualized Volatility")
        ax.set_xlabel("Time")
        ax.set_ylabel("Volatility")
        ax.legend()
        fig.tight_layout()
        fig.savefig(visuals_dir / "04_rolling_volatility.png", dpi=140)
        plt.close(fig)

        # 5) Correlation heatmap.
        fig, ax = plt.subplots(figsize=(8, 6))
        matrix = self.correlation_matrix.values
        im = ax.imshow(matrix, cmap="coolwarm", vmin=-1, vmax=1)
        ax.set_xticks(range(len(COINS)))
        ax.set_xticklabels([coin.title() for coin in COINS])
        ax.set_yticks(range(len(COINS)))
        ax.set_yticklabels([coin.title() for coin in COINS])
        ax.set_title("Price Correlation Matrix")
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", color="black")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        fig.tight_layout()
        fig.savefig(visuals_dir / "05_correlation_heatmap.png", dpi=140)
        plt.close(fig)

    def export_outputs(self) -> None:
        if self.market_data is None or self.price_returns is None or self.summary_table is None:
            raise RuntimeError("Not all outputs are ready for export")

        self.market_data.to_csv(self.output_dir / "market_data_cleaned.csv", index=False)
        self.price_returns.to_csv(self.output_dir / "market_data_with_returns.csv", index=False)
        self.summary_table.to_csv(self.output_dir / "asset_summary.csv", index=False)
        self.correlation_matrix.to_csv(self.output_dir / "price_correlation.csv")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run crypto market intelligence workflow")
    parser.add_argument("--days", type=int, default=30, help="Historical days to fetch from CoinGecko")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory to save csv outputs and visuals",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    pipeline = CryptoMarketPipeline(days=args.days, output_dir=args.output_dir)
    pipeline.fetch_all(COINS)
    pipeline.prepare_market_table()
    pipeline.compute_returns_and_risk()
    pipeline.build_summary()
    pipeline.make_visualizations()
    pipeline.export_outputs()

    print("Workflow completed successfully.")
    print(f"Outputs saved in: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
