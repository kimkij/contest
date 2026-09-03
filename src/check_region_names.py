import pandas as pd

# Check region names in KOSIS
for name, path in [("Disabled", "data/kosis_disabled_sigungu_2023.csv"), 
                   ("Elderly", "data/kosis_elderly_sigungu_2023.csv"), 
                   ("Fiscal", "data/kosis_fiscal_sigungu_2023.csv")]:
    df = pd.read_csv(path)
    regions = [c for c in df['C1_NM'].unique() if "전북" in str(c) or "전라북도" in str(c) or "제주" in str(c)]
    print(f"[{name}] Matching regions:", regions)
