import pandas as pd
from collections import Counter
from scipy.stats import chi2_contingency

iot_data = {
    "app1": Counter({"linear": 2, "relative": 1, "nested": 0, "button": 3, "textview": 2}),
    "app2": Counter({"linear": 0, "relative": 0, "nested": 3, "button": 2, "textview": 1}),
    "app3": Counter({"linear": 1, "relative": 2, "nested": 0, "button": 1, "textview": 3}),
    "app4": Counter({"linear": 1, "relative": 2, "nested": 1, "button": 2, "textview": 3}),
    "app5": Counter({"linear": 2, "relative": 0, "nested": 1, "textview": 2, "button": 1}),
}
non_iot_data = {
    "app1": Counter({"linear": 3, "relative": 0, "nested": 1, "button": 4, "textview": 0}),
    "app2": Counter({"linear": 1, "relative": 2, "nested": 1, "button": 1, "textview": 2}),
    "app3": Counter({"linear": 1, "relative": 0, "nested": 2, "textview": 3, "button": 0}),
    "app4": Counter({"linear": 1, "relative": 1, "nested": 2, "button": 2, "textview": 1}),
    "app5": Counter({"linear": 1, "relative": 1, "nested": 0, "button": 1, "textview": 1}),
}

# Convert data to DataFrames
iot_df = pd.DataFrame.from_dict(iot_data, orient="index").fillna(0)
non_iot_df = pd.DataFrame.from_dict(non_iot_data, orient="index").fillna(0)

# Perform chi-square test for each pair of columns separately
results = {}
for col in iot_df.columns:
    chi2, pval, dof, expected = chi2_contingency(pd.crosstab(iot_df[col], non_iot_df[col]))
    results[col] = {'chi2': chi2, 'p-value': pval, 'dof': dof}

# Print results for each column pair
for col, result in results.items():
    print(f"Chi-square test for '{col}' occurrences:")
    print(f"chi2: {result['chi2']:.4f}, p-value: {result['p-value']:.4f}, dof: {result['dof']}")
