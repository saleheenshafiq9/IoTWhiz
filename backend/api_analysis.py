from pymongo import MongoClient
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import os

# Establish a connection to the MongoDB instance
client = MongoClient('mongodb://localhost:27017/')
db = client['iotWhiz']
collection = db['upload_folder_data']

def calculate_stats():
    iot_data = collection.find({'iot_enabled': True}, {'total_usages': 1, '_id': 0})
    non_iot_data = collection.find({'iot_enabled': False}, {'total_usages': 1, '_id': 0})

    iot_api_usages = [data['total_usages'] for data in iot_data]
    non_iot_api_usages = [data['total_usages'] for data in non_iot_data]

    iot_df = pd.DataFrame({"api_usages": iot_api_usages})
    non_iot_df = pd.DataFrame({"api_usages": non_iot_api_usages})

    t_statistic, p_value = stats.ttest_ind(iot_df["api_usages"], non_iot_df["api_usages"])

    alpha = 0.05
    if p_value < alpha:
        verdict = "There is a significant difference between IoT and Non-IoT API usages."
    else:
        verdict = "There is no significant difference between IoT and Non-IoT API usages."

    return {
        "IoT_Stats": get_stats_output(iot_df, "IoT Apps"),
        "Non_IoT_Stats": get_stats_output(non_iot_df, "Non-IoT Apps"),
        "Verdict": verdict,
        "Histogram": generate_histogram(iot_df, non_iot_df)
    }

# Functions to generate output as requested
def get_stats_output(df, category):
    count = len(df)
    mean = df["api_usages"].mean()
    std_dev = df["api_usages"].std()
    minimum = df["api_usages"].min()
    q1 = df["api_usages"].quantile(0.25)
    median = df["api_usages"].median()
    q3 = df["api_usages"].quantile(0.75)
    maximum = df["api_usages"].max()

    output = f"For {category}:\n"
    output += f"Count: {count} observations.\n"
    output += f"Mean: The mean API usages for {category.lower()} is approximately {mean:.2f}.\n"
    output += f"Standard Deviation (std): The variability in API usages is relatively high with a standard deviation of around {std_dev:.2f}.\n"
    output += f"Minimum: The minimum API usage observed is {minimum}.\n"
    output += f"25th Percentile (Q1): {q1:.1f}, Median (50th percentile or Q2): {median:.1f}, 75th Percentile (Q3): {q3:.1f}.\n"
    output += f"Maximum: The maximum observed API usage for {category.lower()} is {maximum}.\n\n"
    return output

def generate_histogram(iot_df, non_iot_df):
# Plotting histogram
    plt.hist(iot_df["api_usages"], bins=20, label="IoT Apps", alpha=0.5)
    plt.hist(non_iot_df["api_usages"], bins=20, label="Non-IoT Apps", alpha=0.5)
    plt.legend()
    plt.xlabel("Number of API Usages")
    plt.ylabel("Frequency")
    plt.title("Distribution of API Usages in IoT and Non-IoT Apps")

    # Define the relative path to the public directory from the backend directory
    relative_path = os.path.join('..', 'iotwhiz', 'public', 'histogram.png')

    # Save the histogram image to a file using the relative path
    plt.savefig(relative_path)
    plt.close()  # Close the plot to free memory
