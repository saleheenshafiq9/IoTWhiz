from pymongo import MongoClient
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# Establish a connection to the MongoDB instance
client = MongoClient('mongodb://localhost:27017/')
db = client['iotWhiz']
reflection_data = db['reflection_data']

pd.set_option('display.max_columns', None)

# Querying reflection_data table
iot_reflections = reflection_data.find({'iot_enabled': True})
non_iot_reflections = reflection_data.find({'iot_enabled': False})

# Converting MongoDB cursor objects to DataFrames
df_iot = pd.DataFrame(list(iot_reflections))
df_non_iot = pd.DataFrame(list(non_iot_reflections))

df_iot_reflections = df_iot['reflections_summary'].apply(pd.Series)
df_non_iot_reflections = df_non_iot['reflections_summary'].apply(pd.Series)

# Filtering columns and converting to numeric (assuming 'count' and 'Total_Reflections' are relevant columns)
columns_to_keep = ["Class_Loading", "Method_Retrieval", "Instance_Creation", "Method_Invocation", "Field_Retrieval", "Access_Control", "Annotations_Retrieval"]
for column in columns_to_keep:
    df_iot_reflections[column] = df_iot_reflections[column].apply(lambda x: x['count'] if isinstance(x, dict) and 'count' in x else None)
    df_non_iot_reflections[column] = df_non_iot_reflections[column].apply(lambda x: x['count'] if isinstance(x, dict) and 'count' in x else None)


selected_columns_iot = df_iot_reflections[columns_to_keep]
selected_columns_non_iot = df_non_iot_reflections[columns_to_keep]

selected_columns_iot = selected_columns_iot.apply(pd.to_numeric, errors='coerce')
selected_columns_non_iot = selected_columns_non_iot.apply(pd.to_numeric, errors='coerce')

# Adding a column to indicate the type of app (IoT or non-IoT)
df_iot_reflections["App_Type"] = "IoT"
df_non_iot_reflections["App_Type"] = "Non-IoT"

# Combine the two DataFrames
df = pd.concat([df_iot_reflections, df_non_iot_reflections], axis=0, ignore_index=True)

# Perform statistical analysis
print(df.groupby("App_Type").describe())

# T-tests to compare the means of each category between IoT and non-IoT apps
for col in df.columns:
    if col != "App_Type":
        print(f"\n\nT-test for {col}:")
        t, p = stats.ttest_ind(df[col][df["App_Type"] == "IoT"], df[col][df["App_Type"] == "Non-IoT"])
        print(f"t-statistic: {t}")
        print(f"p-value: {p}")

        # Verdict based on p-value
        alpha = 0.05
        if p < alpha:
            print("Verdict: There's a significant difference between IoT and Non-IoT groups for this category.")
        else:
            print("Verdict: No significant difference found between IoT and Non-IoT groups for this category.")

# Visualizations
fig, axes = plt.subplots(1, len(columns_to_keep[:-1]), figsize=(15, 6))

for i, col in enumerate(columns_to_keep[:-1]):
    df.boxplot(column=col, by="App_Type", ax=axes[i])
    axes[i].set_title(f"{col}")
    axes[i].set_xlabel("App Type")
    axes[i].set_ylabel("Count")

plt.suptitle("Comparison of Reflection Usage in IoT and Non-IoT Apps")
plt.tight_layout()
plt.show()
