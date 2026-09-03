import pandas as pd
import json

sido = pd.read_csv("data/sido_master_complete.csv", encoding="utf-8-sig")
gg = pd.read_csv("data/gyeonggi_master_analysis.csv", encoding="utf-8-sig").dropna(subset=['low_floor_route_ratio', 'vulnerable_rate', 'fiscal_rate'])

# Clean and round
sido_records = []
for _, r in sido.iterrows():
    sido_records.append({
        "region": str(r['region']),
        "total_rate": round(float(r['total_rate']), 1),
        "city_bus_rate": round(float(r['city_bus_rate']), 1),
        "vulnerable_rate": round(float(r['vulnerable_rate']), 1),
        "disabled_rate": round(float(r['disabled_rate']), 2),
        "elderly_rate": round(float(r['elderly_rate']), 1),
        "fiscal_rate": round(float(r['fiscal_rate']), 1),
        "total_low": int(r['total_low']),
        "total_pop": int(r['total_pop']) if pd.notnull(r['total_pop']) else 0
    })

gg_records = []
for _, r in gg.iterrows():
    gg_records.append({
        "city": str(r['관할시군']),
        "total_routes": int(r['total_routes']),
        "low_floor_routes": int(r['low_floor_routes']),
        "low_floor_route_ratio": round(float(r['low_floor_route_ratio']), 1),
        "vulnerable_rate": round(float(r['vulnerable_rate']), 1),
        "disabled_rate": round(float(r['disabled_rate']), 2),
        "elderly_rate": round(float(r['elderly_rate']), 1),
        "fiscal_rate": round(float(r['fiscal_rate']), 1),
        "total_pop": int(r['total_pop']) if pd.notnull(r['total_pop']) else 0
    })

with open("results/sido_data.json", "w", encoding="utf-8") as f:
    json.dump(sido_records, f, ensure_ascii=False, indent=2)

with open("results/gg_data.json", "w", encoding="utf-8") as f:
    json.dump(gg_records, f, ensure_ascii=False, indent=2)

print("Exported JSON datasets successfully!")
print("Sido count:", len(sido_records), "GG count:", len(gg_records))
