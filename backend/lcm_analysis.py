import pandas as pd
from pymongo import MongoClient
from scipy import stats
import matplotlib.pyplot as plt
import os

client = MongoClient('mongodb://localhost:27017/')
db = client['iotWhiz_new']
collection = db['loc_class_method_data']

def calculate_lcm():
    # Fetching IoT and non-IoT data based on 'iot_enabled' attribute
    iot_data_mongo = collection.find({'iot_enabled': True})
    non_iot_data_mongo = collection.find({'iot_enabled': False})

    iot_data_from_mongo = pd.DataFrame(list(iot_data_mongo))
    non_iot_data_from_mongo = pd.DataFrame(list(non_iot_data_mongo))

    # Filter out non-numeric columns
    numeric_columns_iot = iot_data_from_mongo.select_dtypes(include=[int, float]).columns
    numeric_columns_non_iot = non_iot_data_from_mongo.select_dtypes(include=[int, float]).columns

    iot_data_numeric = iot_data_from_mongo[numeric_columns_iot]
    non_iot_data_numeric = non_iot_data_from_mongo[numeric_columns_non_iot]

    return {
        "iot_data_numeric": iot_data_numeric.describe(), 
        "non_iot_data": non_iot_data_numeric.describe()
    }

def lcm_inferential():
    # Fetching IoT and non-IoT data based on 'iot_enabled' attribute
    iot_data_mongo = collection.find({'iot_enabled': True})
    non_iot_data_mongo = collection.find({'iot_enabled': False})

    iot_data_from_mongo = pd.DataFrame(list(iot_data_mongo))
    non_iot_data_from_mongo = pd.DataFrame(list(non_iot_data_mongo))

    # Filter out non-numeric columns
    numeric_columns_iot = iot_data_from_mongo.select_dtypes(include=[int, float]).columns
    numeric_columns_non_iot = non_iot_data_from_mongo.select_dtypes(include=[int, float]).columns

    iot_data_numeric = iot_data_from_mongo[numeric_columns_iot]
    non_iot_data_numeric = non_iot_data_from_mongo[numeric_columns_non_iot]

    # Comparison of means using t-test
    inferential_results = {}
    for column in numeric_columns_iot:
        t, p = stats.ttest_ind(iot_data_numeric[column], non_iot_data_numeric[column])
        significance_level = 0.05  # You can change the significance level if needed
        if p < significance_level:
            verdict = f"There is a significant difference in the means of IoT & non-IoT apps in terms of {column}"
        else:
            verdict = f"No significant difference in the means of IoT & non-IoT apps in terms of {column}"

        inferential_results[column] = {
            "t_statistic": t,
            "p_value": p,
            "verdict": verdict
        }

    # Correlation analysis
    iot_corr_matrix = iot_data_numeric.corr()
    non_iot_corr_matrix = non_iot_data_numeric.corr()

    boxplot_paths = []
    scatterplot_paths = []

    # Save Boxplots
    for column in numeric_columns_iot:
        fig, ax = plt.subplots()
        ax.boxplot([iot_data_numeric[column], non_iot_data_numeric[column]], labels=["IoT", "Non-IoT"])
        ax.set_title(f"Boxplot of {column}")
        current_directory = os.path.dirname(os.path.abspath(__file__))
        plot_path = os.path.join(current_directory, f"boxplot_{column}.png")  # Replace 'path_to_save' with your desired path
        fig.savefig(plot_path)
        plt.close(fig)
        boxplot_paths.append(plot_path)

    # Save Scatter plots
    for i in range(len(numeric_columns_iot)):
        for j in range(i + 1, len(numeric_columns_iot)):
            fig, ax = plt.subplots()
            ax.scatter(iot_data_numeric[numeric_columns_iot[i]], iot_data_numeric[numeric_columns_iot[j]], color="blue", label="IoT")
            ax.scatter(non_iot_data_numeric[numeric_columns_iot[i]], non_iot_data_numeric[numeric_columns_iot[j]], color="red", label="Non-IoT")
            ax.set_xlabel(numeric_columns_iot[i])
            ax.set_ylabel(numeric_columns_iot[j])
            ax.legend()
            ax.set_title(f"Scatter plot of {numeric_columns_iot[i]} vs. {numeric_columns_iot[j]}")
            current_directory = os.path.dirname(os.path.abspath(__file__))
            plot_path = os.path.join(current_directory, f"scatterplot_{numeric_columns_iot[i]}_vs_{numeric_columns_iot[j]}.png")  # Replace 'path_to_save' with your desired path
            fig.savefig(plot_path)
            plt.close(fig)
            scatterplot_paths.append(plot_path)

    return {
        "inferential_results": inferential_results,
        "iot_correlation_matrix": iot_corr_matrix.to_dict(),
        "non_iot_correlation_matrix": non_iot_corr_matrix.to_dict(),
        "boxplot_paths": boxplot_paths,
        "scatterplot_paths": scatterplot_paths
    }