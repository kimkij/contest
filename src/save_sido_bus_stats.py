import pandas as pd
import json

# Let's parse Page 43 [표 3-3] into a clean structured CSV
data = [
    {"region": "서울특별시", "city_bus_low": 4926, "city_bus_rate": 66.7, "rural_bus_low": 0, "rural_bus_rate": 0.0, "village_bus_low": 161, "village_bus_rate": 10.3, "total_low": 5087, "total_rate": 56.8},
    {"region": "부산광역시", "city_bus_low": 917, "city_bus_rate": 36.4, "rural_bus_low": 0, "rural_bus_rate": 0.0, "village_bus_low": 6, "village_bus_rate": 1.1, "total_low": 923, "total_rate": 29.9},
    {"region": "대구광역시", "city_bus_low": 728, "city_bus_rate": 46.5, "rural_bus_low": 0, "rural_bus_rate": 0.0, "village_bus_low": 0, "village_bus_rate": 0.0, "total_low": 728, "total_rate": 46.1},
    {"region": "인천광역시", "city_bus_low": 412, "city_bus_rate": 18.8, "rural_bus_low": 0, "rural_bus_rate": 0.0, "village_bus_low": 0, "village_bus_rate": 0.0, "total_low": 412, "total_rate": 18.6},
    {"region": "광주광역시", "city_bus_low": 394, "city_bus_rate": 37.7, "rural_bus_low": 0, "rural_bus_rate": 0.0, "village_bus_low": 0, "village_bus_rate": 0.0, "total_low": 394, "total_rate": 34.8},
    {"region": "대전광역시", "city_bus_low": 412, "city_bus_rate": 39.7, "rural_bus_low": 0, "rural_bus_rate": 0.0, "village_bus_low": 0, "village_bus_rate": 0.0, "total_low": 412, "total_rate": 39.0},
    {"region": "울산광역시", "city_bus_low": 127, "city_bus_rate": 14.6, "rural_bus_low": 0, "rural_bus_rate": 0.0, "village_bus_low": 0, "village_bus_rate": 0.0, "total_low": 127, "total_rate": 13.8},
    {"region": "세종특별자치시", "city_bus_low": 123, "city_bus_rate": 46.4, "rural_bus_low": 0, "rural_bus_rate": 0.0, "village_bus_low": 0, "village_bus_rate": 0.0, "total_low": 123, "total_rate": 41.3},
    {"region": "경기도", "city_bus_low": 3442, "city_bus_rate": 32.1, "rural_bus_low": 10, "rural_bus_rate": 7.1, "village_bus_low": 727, "village_bus_rate": 26.6, "total_low": 4179, "total_rate": 30.7},
    {"region": "강원특별자치도", "city_bus_low": 204, "city_bus_rate": 41.9, "rural_bus_low": 15, "rural_bus_rate": 7.4, "village_bus_low": 0, "village_bus_rate": 0.0, "total_low": 219, "total_rate": 26.1},
    {"region": "충청북도", "city_bus_low": 217, "city_bus_rate": 33.3, "rural_bus_low": 4, "rural_bus_rate": 1.9, "village_bus_low": 0, "village_bus_rate": 0.0, "total_low": 221, "total_rate": 25.4},
    {"region": "충청남도", "city_bus_low": 196, "city_bus_rate": 21.7, "rural_bus_low": 2, "rural_bus_rate": 0.8, "village_bus_low": 0, "village_bus_rate": 0.0, "total_low": 198, "total_rate": 16.5},
    {"region": "전라북도", "city_bus_low": 259, "city_bus_rate": 30.5, "rural_bus_low": 4, "rural_bus_rate": 2.7, "village_bus_low": 0, "village_bus_rate": 0.0, "total_low": 263, "total_rate": 24.8},
    {"region": "전라남도", "city_bus_low": 137, "city_bus_rate": 20.3, "rural_bus_low": 13, "rural_bus_rate": 2.2, "village_bus_low": 0, "village_bus_rate": 0.0, "total_low": 150, "total_rate": 11.5},
    {"region": "경상북도", "city_bus_low": 277, "city_bus_rate": 22.7, "rural_bus_low": 1, "rural_bus_rate": 0.4, "village_bus_low": 0, "village_bus_rate": 0.0, "total_low": 278, "total_rate": 18.0},
    {"region": "경상남도", "city_bus_low": 672, "city_bus_rate": 37.9, "rural_bus_low": 17, "rural_bus_rate": 7.4, "village_bus_low": 3, "village_bus_rate": 2.8, "total_low": 692, "total_rate": 32.8},
    {"region": "제주특별자치도", "city_bus_low": 157, "city_bus_rate": 18.9, "rural_bus_low": 0, "rural_bus_rate": 0.0, "village_bus_low": 2, "village_bus_rate": 5.1, "total_low": 159, "total_rate": 18.3}
]

df = pd.DataFrame(data)
df.to_csv("data/low_floor_bus_2023_by_sido.csv", index=False, encoding="utf-8-sig")
print("Saved data/low_floor_bus_2023_by_sido.csv successfully!")
print(df.head())
