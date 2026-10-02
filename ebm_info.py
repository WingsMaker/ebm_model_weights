import pickle
import json
import numpy as np

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
bins = model.bins_
intercept = model.intercept_[0] if isinstance(model.intercept_, (list, np.ndarray)) else model.intercept_

with open(json_file, "w") as g:
    output = dict()
    output["Global_Intercept"] = intercept
    for idx, name in enumerate(term_names):
        weights = term_scores[idx]
        output[name] = {
            "scores": weights.tolist()
        }    
    json.dump(output, g, indent=2)
print(f"model weights file {json_file} created.")