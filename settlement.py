import pandas as pd
import glob, os
from datetime import datetime

# === Configuration ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(BASE_DIR, "Settlement_Raw")       # folder with your daily CSVs
output_folder = os.path.join(BASE_DIR, "Settlement_Output")  # output folder
os.makedirs(output_folder, exist_ok=True)

# === Step 1: Load and combine all CSVs ===
all_files = sorted(glob.glob(os.path.join(data_folder, "*.csv")))
dfs = []

for f in all_files:
    date_str = f.split("_")[-1].replace(".csv", "")
    try:
        file_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print(f"⚠️ Skipping {f} (invalid date)")
        continue

    df = pd.read_csv(f, thousands=",", encoding_errors="ignore")
    df.columns = df.columns.str.strip().str.replace('\u00A0', ' ', regex=True)
    df["Date"] = file_date
    dfs.append(df)

if not dfs:
    raise SystemExit("❌ No valid CSVs found in Settlement_Raw/")

df = pd.concat(dfs, ignore_index=True)
df["Date"] = pd.to_datetime(df["Date"])

# === Step 2: Ensure numeric columns ===
numeric_cols = [
    "Trade Volume", "Trade Value",
    "UIN Settlement Volume", "UIN Settlement Value",
    "UIN Percentage Volume", "UIN Percentage Value"
]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# === Step 3: Save combined daily ===
daily_path = os.path.join(output_folder, "combined_daily.csv")
df.to_csv(daily_path, index=False)
print(f"✅ Combined daily data saved: {daily_path}")

# === Step 4: Weekly aggregation (week ends on Friday) ===
weekly = (
    df.groupby(["Symbol", pd.Grouper(key="Date", freq="W-FRI")])  # <- Friday week-end
    .agg({
        "Trade Volume": "sum",
        "Trade Value": "sum",
        "UIN Settlement Volume": "sum",
        "UIN Settlement Value": "sum"
    })
    .reset_index()
)

weekly["UIN % Volume"] = weekly["UIN Settlement Volume"] / weekly["Trade Volume"] * 100
weekly["UIN % Value"]   = weekly["UIN Settlement Value"]   / weekly["Trade Value"]   * 100

weekly_path = os.path.join(output_folder, "aggregated_weekly.csv")
weekly.to_csv(weekly_path, index=False)
print(f"✅ Weekly summary saved: {weekly_path}")


# === Step 5: Monthly aggregation ===
monthly = (
    df.groupby(["Symbol", pd.Grouper(key="Date", freq="M")])
    .agg({
        "Trade Volume": "sum",
        "Trade Value": "sum",
        "UIN Settlement Volume": "sum",
        "UIN Settlement Value": "sum"
    })
    .reset_index()
)
monthly["UIN % Volume"] = monthly["UIN Settlement Volume"] / monthly["Trade Volume"] * 100
monthly["UIN % Value"] = monthly["UIN Settlement Value"] / monthly["Trade Value"] * 100

monthly_path = os.path.join(output_folder, "aggregated_monthly.csv")
monthly.to_csv(monthly_path, index=False)
print(f"✅ Monthly summary saved: {monthly_path}")
