from pymongo import MongoClient
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os

def calculate_dynamic_stats():
    # Connect to MongoDB and fetch data
    client = MongoClient('mongodb://localhost:27017/')
    db = client['iotWhiz_new']
    collection = db['upload_folder_data']

    iot_data = collection.find({'iot_enabled': True})
    non_iot_data = collection.find({'iot_enabled': False})

    # Extract 'total_dynamic_usages' for IoT and non-IoT apps
    iot_dynamic_usages = [entry['total_dynamic_usages'] for entry in iot_data]
    non_iot_dynamic_usages = [entry['total_dynamic_usages'] for entry in non_iot_data]

    # Create dataframes
    iot_df = pd.DataFrame(data={"dynamic_class_loading": iot_dynamic_usages})
    non_iot_df = pd.DataFrame(data={"dynamic_class_loading": non_iot_dynamic_usages})

    # Perform statistical analysis
    iot_count = len(iot_dynamic_usages)
    non_iot_count = len(non_iot_dynamic_usages)

    iot_mean = round(iot_df["dynamic_class_loading"].mean(), 2)
    non_iot_mean = round(non_iot_df["dynamic_class_loading"].mean(), 2)

    iot_std = round(iot_df["dynamic_class_loading"].std(), 2)
    non_iot_std = round(non_iot_df["dynamic_class_loading"].std(), 2)

    iot_min = iot_df["dynamic_class_loading"].min()
    non_iot_min = non_iot_df["dynamic_class_loading"].min()

    iot_q1, iot_median, iot_q3 = iot_df["dynamic_class_loading"].quantile([0.25, 0.5, 0.75])
    non_iot_q1, non_iot_median, non_iot_q3 = non_iot_df["dynamic_class_loading"].quantile([0.25, 0.5, 0.75])

    iot_max = iot_df["dynamic_class_loading"].max()
    non_iot_max = non_iot_df["dynamic_class_loading"].max()

    # Hypothesis testing
    t_statistic, p_value = stats.ttest_ind(
        iot_df["dynamic_class_loading"], non_iot_df["dynamic_class_loading"]
    )

    # Interpretation
    if p_value < 0.05:
        verdict = "There is a statistically significant difference in the mean dynamic class loading usage between IoT and non-IoT apps."
    else:
        verdict = "There is no statistically significant difference in the mean dynamic class loading usage between IoT and non-IoT apps."

    # Generate histograms
    plt.boxplot(
        [iot_df["dynamic_class_loading"], non_iot_df["dynamic_class_loading"]],
        labels=["IoT", "Non-IoT"]
    )
    plt.xlabel("App type")
    plt.ylabel("Dynamic class loading usage")
    plt.title("Comparison of dynamic class loading usage between IoT and non-IoT apps")
    current_directory = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(current_directory, 'dc_histogram.png')    
    plt.savefig(relative_path)
    plt.close()
    return {
        "IoT_Stats": get_stats_output(iot_count, iot_mean, iot_std, iot_min, iot_q1, iot_median, iot_q3, iot_max, "IoT Apps"),
        "Non_IoT_Stats": get_stats_output(non_iot_count, non_iot_mean, non_iot_std, non_iot_min, non_iot_q1, non_iot_median, non_iot_q3, non_iot_max, "Non-IoT Apps"),
        "Verdict": verdict,
        "Histogram": relative_path,
    }

# Function to format statistics output
def get_stats_output(count, mean, std_dev, minimum, q1, median, q3, maximum, category):
    output = f"For {category}:\n"
    output += f"Count: {count} observations.\n"
    output += f"Mean: The mean dynamic class loading usage for {category.lower()} is approximately {mean}.\n"
    output += f"Standard Deviation (std): The variability in dynamic class loading is relatively high with a standard deviation of around {std_dev}.\n"
    output += f"Minimum: The minimum dynamic class loading observed is {minimum}.\n"
    output += f"25th Percentile (Q1): {q1}, Median (50th percentile or Q2): {median}, 75th Percentile (Q3): {q3}.\n"
    output += f"Maximum: The maximum dynamic class loading observed for {category.lower()} is {maximum}.\n\n"
    return output

# # Execute the function to get stats and visualizations
# result = calculate_dynamic_stats()
# print(result)  # Optional: print the result
