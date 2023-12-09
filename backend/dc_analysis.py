from pymongo import MongoClient
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming you've fetched data from MongoDB and stored it in the variable `data`
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['iotWhiz']
collection = db['upload_folder_data']

# Fetch data from MongoDB based on IoT enabled status
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

# Output analysis
print(f"Count: Both datasets have {iot_count} observations.")
print(f"Mean: For IoT apps, the mean dynamic class loading usage is approximately {iot_mean}, while for non-IoT apps, it's around {non_iot_mean}.")
print(f"Standard Deviation (std): There's more variability in the dynamic class loading for IoT apps (std approximately {iot_std}) compared to non-IoT apps (std approximately {non_iot_std}).")
print(f"Minimum: The minimum value for IoT is {iot_min} and non-IoT apps is {non_iot_min}.")
print(f"25th Percentile (Q1), Median (50th percentile or Q2), 75th Percentile (Q3):")
print(f"These quartiles show the distribution of the data. For example, in IoT apps, 25% of the observations fall below {iot_q1}, 50% fall below {iot_median}, and 75% fall below {iot_q3}. Similarly for non-IoT apps, 25% fall below {non_iot_q1}, 50% fall below {non_iot_median}, and 75% fall below {non_iot_q3}.")
print(f"Maximum: The maximum value for IoT apps is {iot_max}, and for non-IoT apps, it's {non_iot_max}.")

# Hypothesis testing
# Check if the means are equal
from scipy import stats

t_statistic, p_value = stats.ttest_ind(
    iot_df["dynamic_class_loading"], non_iot_df["dynamic_class_loading"]
)

print(f"\nT-statistic: {t_statistic:.4f}")
print(f"P-value: {p_value:.4f}")

# Interpretation
if p_value < 0.05:
    print(
        "\nThere is a statistically significant difference in the mean dynamic class loading usage between IoT and non-IoT apps."
    )
else:
    print(
        "\nThere is no statistically significant difference in the mean dynamic class loading usage between IoT and non-IoT apps."
    )

# Additional analysis
# Visualize the data using boxplots
import matplotlib.pyplot as plt

plt.boxplot(
    [iot_df["dynamic_class_loading"], non_iot_df["dynamic_class_loading"]], labels=["IoT", "Non-IoT"]
)
plt.xlabel("App type")
plt.ylabel("Dynamic class loading usage")
plt.title("Comparison of dynamic class loading usage between IoT and non-IoT apps")
plt.show()

# Analyze the distribution of the data
import seaborn as sns

sns.distplot(iot_df["dynamic_class_loading"], label="IoT")
sns.distplot(non_iot_df["dynamic_class_loading"], label="Non-IoT")
plt.xlabel("Dynamic class loading usage")
plt.ylabel("Density")
plt.title("Distribution of dynamic class loading usage")
plt.legend()
plt.show()
