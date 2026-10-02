Markdown
# EBM Model Weight Export Script - Explanation
 
This script loads a serialized **Explainable Boosting Machine (EBM)** model from a pickle (`.pkl`) file, extracts the model's learned weights, and exports them to a JSON file for easier inspection and downstream use.
 
---
 
## 1. Import Required Libraries
 
```python
import pickle
import json
import numpy as np
```
 
### Purpose
 
- `pickle` : Loads serialized Python objects from a `.pkl` file.
- `json` : Writes extracted model information to a JSON file.
- `numpy` : Used to identify NumPy arrays.
 
> **Note:** The script uses `sys.argv` but is missing:
>
> ```python
> import sys
> ```
 
---
 
## 2. Validate Command Line Input
 
```python
if len(sys.argv) < 2:
print("Usage: python ebm_info.py <pickle_file_path>")
sys.exit(1)
```
 
### What it does
 
The script expects a pickle file path as a command-line argument.
 
Example:
 
```bash
python ebm_info.py fraud_model.pkl
```
 
If no file path is provided, the script displays:
 
```text
Usage: python ebm_info.py <pickle_file_path>
```
 
and exits.
 
---
 
## 3. Define Input and Output Files
 
```python
pickle_file_path = sys.argv[1]
json_file = pickle_file_path.replace(".pkl",".json")
```
 
### Example
 
Input file:
 
```text
fraud_model.pkl
```
 
Output file:
 
```text
fraud_model.json
```
 
---
 
## 4. Load the Pickled EBM Model
 
```python
with open(pickle_file_path, "rb") as f:
ebm = pickle.load(f)
```
 
### What happens
 
The trained EBM model is deserialized and loaded into memory.
 
After this step:
 
```python
ebm
```
 
contains the full saved model object.
 
---
 
## 5. Extract Model Components
 
```python
model = ebm.model
```
 
The code assumes the loaded object contains a `.model` attribute.
 
The following EBM attributes are extracted:
 
```python
term_names = model.term_names_
term_features = model.term_features_
term_scores = model.term_scores_
bins = model.bins_
```
 
### Meaning of Each Attribute
 
#### `term_names_`
 
Contains feature names and interaction names.
 
Example:
 
```python
[
"age",
"income",
"loan_amount"
]
```
 
---
 
#### `term_features_`
 
Maps each term to one or more feature indexes.
 
Example:
 
```python
[
(0,),
(1,),
(2,)
]
```
 
Meaning:
 
| Term | Feature Index |
|--------|--------|
| age | 0 |
| income | 1 |
| loan_amount | 2 |
 
For interactions:
 
```python
[(0, 1)]
```
 
represents:
 
```text
age × income
```
 
---
 
#### `term_scores_`
 
Stores the learned score values for each feature bin.
 
Example:
 
```python
[
[-0.3, 0.2, 0.5],
[0.1, 0.4, -0.2]
]
```
 
Each value represents the EBM contribution for a particular bin.
 
---
 
#### `bins_`
 
Contains bin definitions created during model training.
 
Example:
 
```python
[
[20, 30, 40, 50]
]
```
 
Meaning:
 
```text
age < 20
20–30
30–40
40–50
50+
```
 
Although extracted, `bins_` is not used later in the script.
 
---
 
## 6. Extract the Global Intercept
 
```python
intercept = model.intercept_[0] if isinstance(model.intercept_, (list, np.ndarray)) else model.intercept_
```
 
### Why this is needed
 
Different EBM versions may store the intercept as:
 
```python
0.72
```
 
or
 
```python
[0.72]
```
 
or
 
```python
array([0.72])
```
 
This line ensures the result is always a scalar value:
 
```python
intercept = 0.72
```
 
---
 
## 7. Prepare the Output Dictionary
 
```python
with open(json_file, "w") as g:
output = dict()
```
 
Creates an empty output structure:
 
```python
output = {}
```
 
---
 
### Add Global Intercept
 
```python
output["Global_Intercept"] = intercept
```
 
Result:
 
```python
{
"Global_Intercept": 0.72
}
```
 
---
 
## 8. Export Term Scores
 
```python
for idx, name in enumerate(term_names):
```
 
Iterates through every EBM term.
 
Example:
 
```python
idx = 0
name = "age"
```
 
Retrieve the corresponding scores:
 
```python
weights = term_scores[idx]
```
 
Example:
 
```python
weights = [-0.5, -0.1, 0.2, 0.7]
```
 
Store them in the output dictionary:
 
```python
output[name] = {
"scores": weights.tolist()
}
```
 
Result:
 
```python
{
"age": {
"scores": [-0.5, -0.1, 0.2, 0.7]
}
}
```
 
### Why `tolist()`?
 
NumPy arrays cannot be directly serialized into JSON.
 
```python
weights.tolist()
```
 
converts:
 
```python
array([-0.5, -0.1, 0.2, 0.7])
```
 
to:
 
```python
[-0.5, -0.1, 0.2, 0.7]
```
 
---
 
## 9. Write JSON Output
 
```python
json.dump(output, g, indent=2)
```
 
Writes a nicely formatted JSON file.
 
Example output:
 
```json
{
"Global_Intercept": 0.72,
"age": {
"scores": [-0.5, -0.1, 0.2, 0.7]
},
"income": {
"scores": [0.1, 0.3, 0.6, 0.9]
}
}
```
 
---
 
## 10. Print Completion Message
 
```python
print(f"model weights file {json_file} created.")
```
 
Example:
 
```text
model weights file fraud_model.json created.
```
 
---
 
# Information Exported
 
The script exports:
 
✅ Global intercept
 
✅ Feature/term names
 
✅ Term score arrays
 
---
 
# Information Extracted but Not Exported
 
The script reads:
 
```python
term_features_
bins_
```
 
but does not include them in the JSON output.
 
As a result, you can see the scores but cannot determine:
 
- Which feature index generated the scores.
- Which value range each score corresponds to.
- How interaction terms are mapped.
 
For example:
 
```json
{
"age": {
"scores": [-0.2, 0.1, 0.5]
}
}
```
 
does not tell you whether those scores correspond to:
 
```text
age < 20
20 ≤ age < 40
age ≥ 40
```
 
or any other bin definition.
 
---
 
# Possible Improvement
 
To make the JSON fully interpretable, include the feature mappings and bin boundaries:
 
```python
output[name] = {
"features": term_features[idx],
"bins": bins[feature_id],
"scores": weights.tolist()
}
```
 
This would allow each score to be directly mapped back to the feature ranges used during model training.
 
---
 
# Summary
 
The script is an **EBM model inspection utility** that:
 
1. Loads a trained EBM model from a `.pkl` file.
2. Extracts the global intercept and term score arrays.
3. Converts NumPy arrays to JSON-compatible lists.
4. Writes model weights into a JSON file.
5. Produces a simplified representation of the model.
6. Does **not** export bin definitions or feature mappings, limiting full interpretability of the exported scores.
