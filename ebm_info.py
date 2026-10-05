import pickle
import json
import numpy as np
import sys

if len(sys.argv) < 2:
    print("Usage: python ebm_info.py <pickle_file_path>")
    sys.exit(1)
pickle_file_path = sys.argv[1]
json_file = pickle_file_path.replace(".pkl",".json")

with open(pickle_file_path, "rb") as f:
    ebm = pickle.load(f)

model = ebm.model
term_names = model.term_names_
term_features = model.term_features_
term_scores = model.term_scores_
model_bins = model.bins_
intercept = model.intercept_[0] if isinstance(model.intercept_, (list, np.ndarray)) else model.intercept_

output = dict()
output["Global_Intercept"] = intercept
for idx, name in enumerate(term_names):
    weights = term_scores[idx]
    output[name] = {
        "scores": weights.tolist()
    }    
for n in range(len(model_bins)):
    try:
        arr = [ x.tolist() for x in model_bins[n] ]
    except:
        arr = list(model_bins[n])
    for i in range(len(arr)):
        p = f"bin_{n:05d}_{i+1}"
        output[p] = arr[i]

with open(json_file, "w") as g:
    json.dump(output, g, indent=2)
print(f"model weights file {json_file} created.")
