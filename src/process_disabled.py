import pandas as pd

# Load MOHW disabled dataset
df = pd.read_csv("data/mohw_disabled_raw.csv", encoding="cp949")
print("Columns:", list(df.columns))
print("Years:", df.iloc[:, 0].unique())
# filter latest year (2024 or latest)
latest_year = df.iloc[:, 0].max()
df_latest = df[df.iloc[:, 0] == latest_year].copy()
print(f"Latest year ({latest_year}) records:", len(df_latest))
print(df_latest.head())

df_latest.to_csv("data/disabled_population_sido_latest.csv", index=False, encoding="utf-8-sig")
print("Saved data/disabled_population_sido_latest.csv")
