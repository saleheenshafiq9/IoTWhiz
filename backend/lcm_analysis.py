import pandas as pd
from pymongo import MongoClient
from scipy import stats
import matplotlib.pyplot as plt

# Establish a connection to the MongoDB instance
client = MongoClient('mongodb://localhost:27017/')
db = client['iotWhiz']
collection = db['loc_class_method_data']

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

# Descriptive statistics for each DataFrame
print("Descriptive statistics for IoT apps:")
print(iot_data_numeric.describe())
print("\nDescriptive statistics for non-IoT apps:")
print(non_iot_data_numeric.describe())

# Comparison of means using t-test
for column in numeric_columns_iot:
    t, p = stats.ttest_ind(iot_data_numeric[column], non_iot_data_numeric[column])
    print(f"\nComparison of means for {column}:")
    print(f"t-statistic: {t:.4f}, p-value: {p:.4f}")

    significance_level = 0.05  # You can change the significance level if needed
    if p < significance_level:
        print("Verdict: Significant difference - Reject null hypothesis")
    else:
        print("Verdict: No significant difference - Fail to reject null hypothesis")
            
# Correlation analysis
print("\nCorrelation matrix for IoT apps:")
print(iot_data_numeric.corr())
print("\nCorrelation matrix for non-IoT apps:")
print(non_iot_data_numeric.corr())

# Visualization - Boxplots for each variable
for column in numeric_columns_iot:
    plt.boxplot([iot_data_numeric[column], non_iot_data_numeric[column]], labels=["IoT", "Non-IoT"])
    plt.title(f"Boxplot of {column}")
    plt.show()

# Scatter plots for each pair of variables
for i in range(len(numeric_columns_iot)):
    for j in range(i + 1, len(numeric_columns_iot)):
        plt.scatter(iot_data_numeric[numeric_columns_iot[i]], iot_data_numeric[numeric_columns_iot[j]], color="blue", label="IoT")
        plt.scatter(non_iot_data_numeric[numeric_columns_iot[i]], non_iot_data_numeric[numeric_columns_iot[j]], color="red", label="Non-IoT")
        plt.xlabel(numeric_columns_iot[i])
        plt.ylabel(numeric_columns_iot[j])
        plt.legend()
        plt.title(f"Scatter plot of {numeric_columns_iot[i]} vs. {numeric_columns_iot[j]}")
        plt.show()