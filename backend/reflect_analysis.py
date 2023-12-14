from pymongo import MongoClient
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import os

# Establish a connection to the MongoDB instance
client = MongoClient('mongodb://localhost:27017/')
db = client['iotWhiz_new']
reflection_data = db['reflection_data']


def calculate_reflections():
    pd.set_option('display.max_columns', None)
    columns_to_keep = ["Class_Loading", "Method_Retrieval", "Instance_Creation", "Method_Invocation", "Field_Retrieval", "Access_Control", "Annotations_Retrieval"]
    # Querying reflection_data table
    iot_reflections = reflection_data.find({'iot_enabled': True})
    non_iot_reflections = reflection_data.find({'iot_enabled': False})

    # Converting MongoDB cursor objects to DataFrames
    df_iot = pd.DataFrame(list(iot_reflections))
    df_non_iot = pd.DataFrame(list(non_iot_reflections))

    df_iot_reflections = df_iot['reflections_summary'].apply(pd.Series)
    df_non_iot_reflections = df_non_iot['reflections_summary'].apply(pd.Series)

    # Filtering columns and converting to numeric (assuming 'count' and 'Total_Reflections' are relevant columns)

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

    return {
        "descriptive_results" : perform_descriptive_reflection(df),
        "test_results" : perform_statistical_analysis(df),
        "reflection_boxplots" : get_boxplot_image(df)
    }

def perform_descriptive_reflection(df):
# Perform statistical analysis
    return df.groupby("App_Type").describe()

def perform_statistical_analysis(df):
    results = {}
    for col in df.columns:
        if col != "App_Type":
            t, p = stats.ttest_ind(df[col][df["App_Type"] == "IoT"], df[col][df["App_Type"] == "Non-IoT"])
            verdict = f"There is significant difference between IoT & non-IoT apps in terms of {col}" if p < 0.05 else F"No significant difference between IoT & non-IoT apps in terms of {col}"
            results[col] = {
                "t-statistic": t,
                "p-value": p,
                "verdict": verdict
            }
    return results

def get_boxplot_image(df):
    columns_to_keep = ["Class_Loading", "Method_Retrieval", "Instance_Creation", "Method_Invocation", "Field_Retrieval", "Annotations_Retrieval", "Access_Control"]
    # Visualizations
    fig, axes = plt.subplots(1, len(columns_to_keep[:-1]), figsize=(15, 6))
    for i, col in enumerate(columns_to_keep[:-1]):
        df.boxplot(column=col, by="App_Type", ax=axes[i])
        axes[i].set_title(f"{col}")
        axes[i].set_xlabel("App Type")
        axes[i].set_ylabel("Count")

    current_directory = os.path.dirname(os.path.abspath(__file__))
    plot_path = os.path.join(current_directory, "reflect_boxplot.png")

    plt.suptitle("Comparison of Reflection Usage in IoT and Non-IoT Apps")
    plt.savefig(plot_path)

    # plt.show()
    plt.close()

    return plot_path