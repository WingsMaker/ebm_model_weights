import pandas as pd
import json
import sys

# Load JSON
if len(sys.argv) < 2:
    print("Usage: python json2csv.py <json_file_path>")
    sys.exit(1)
json_file_path = sys.argv[1]
with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
csv_file = json_file_path.replace(".json",".csv")

# Convert to DataFrame
df = pd.json_normalize(data)

# Save as Excel
df.to_csv(csv_file, index=False)
print(f"Saved to {csv_file}")
