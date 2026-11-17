"""NYC TLC 2017 Yellow Taxi: exploratory data analysis.

Usage:
    python src/analysis.py [path/to/2017_Yellow_Taxi_Trip_Data.csv]
"""
import sys
from pathlib import Path

import pandas as pd

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data" / "2017_Yellow_Taxi_Trip_Data.csv"

# payment_type codes from the TLC data dictionary
PAYMENT_TYPES = {1: "Credit card", 2: "Cash", 3: "No charge", 4: "Dispute", 5: "Unknown", 6: "Voided trip"}


def load(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def inspect(df: pd.DataFrame) -> None:
    print(df.head(10), "\n")
    df.info()
    print("\n", df.describe(), "\n")


def extremes(df: pd.DataFrame) -> None:
    print("Top 10 by trip_distance:\n", df.sort_values("trip_distance", ascending=False).head(10), "\n")
    print("Top 20 by total_amount:\n", df.sort_values("total_amount", ascending=False).head(20), "\n")
    print("Bottom 20 by total_amount:\n", df.sort_values("total_amount").head(20), "\n")


def summaries(df: pd.DataFrame) -> None:
    pay = df["payment_type"].value_counts(normalize=True).rename(index=PAYMENT_TYPES)
    print("Payment type share:\n", pay, "\n")

    print("Mean tip by payment type:\n",
          df.groupby("payment_type")["tip_amount"].mean().rename(index=PAYMENT_TYPES), "\n")

    print("Trips per vendor:\n", df["VendorID"].value_counts(), "\n")
    print("Mean total_amount per vendor:\n", df.groupby("VendorID")["total_amount"].mean(), "\n")

    credit = df[df["payment_type"] == 1]
    print("Mean tip by passenger_count (credit card only):\n",
          credit.groupby("passenger_count")["tip_amount"].mean(), "\n")

    print("Correlation with total_amount / tip_amount:\n",
          df[["trip_distance", "fare_amount", "passenger_count", "total_amount", "tip_amount"]].corr()[
              ["total_amount", "tip_amount"]], "\n")


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    df = load(path)
    inspect(df)
    extremes(df)
    summaries(df)


if __name__ == "__main__":
    main()
