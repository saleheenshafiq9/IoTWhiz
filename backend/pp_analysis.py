import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter, defaultdict
import pymongo

permission_categories = {
    "INTERNET": "Network Communication",
    "ACCESS_NETWORK_STATE": "Network Communication",
    "CAMERA": "Media and Camera",
    "READ_EXTERNAL_STORAGE": "Storage",
    "WRITE_EXTERNAL_STORAGE": "Storage",
    "ACCESS_FINE_LOCATION": "Location",
    "ACCESS_COARSE_LOCATION": "Location",
    "RECORD_AUDIO": "Audio",
    "MODIFY_AUDIO_SETTINGS": "Audio",
    "READ_CONTACTS": "Contacts",
    "WRITE_CONTACTS": "Contacts",
    "CALL_PHONE": "Phone Calls",
    "BLUETOOTH": "Bluetooth",
    "BLUETOOTH_ADMIN": "Bluetooth",
    "READ_CALENDAR": "Calendar",
    "WRITE_CALENDAR": "Calendar",
    "READ_SMS": "SMS",
    "SEND_SMS": "SMS",
    "RECEIVE_SMS": "SMS",
    "READ_PHONE_STATE": "Phone Information",
    "READ_CALL_LOG": "Phone Calls",
    "WRITE_CALL_LOG": "Phone Calls",
    "ADD_VOICEMAIL": "Phone Calls",
    "USE_SIP": "SIP Services",
    "PROCESS_OUTGOING_CALLS": "Phone Calls",
    "BODY_SENSORS": "Sensors",
    "SEND_RESPOND_VIA_MESSAGE": "Messaging",
    "READ_CELL_BROADCASTS": "Broadcasts",
    "USE_FINGERPRINT": "Biometric",
    "ACTIVITY_RECOGNITION": "Activity Recognition",
    "ACCESS_WIFI_STATE": "Wi-Fi",
    "CHANGE_WIFI_STATE": "Wi-Fi",
    "ACCESS_WIFI_STATE": "Wi-Fi",
    "CHANGE_WIFI_MULTICAST_STATE": "Wi-Fi",
    "VIBRATE": "Notification",
    "WAKE_LOCK": "Notification",
    "GET_ACCOUNTS": "Notification",
    "USE_CREDENTIALS": "Notification",
    "POST_NOTIFICATIONS": "Notification",
    "ACCESS_NOTIFICATION_POLICY": "Notification",
    "SCHEDULE_EXACT_ALARM": "Alarms"
}

# Connect to your MongoDB instance
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["iotWhiz"]
collection = database["upload_folder_data"]

# Query the collection for relevant data
data_from_db = collection.find({})

app_data = []

# Process the retrieved data
for item in data_from_db:
    app_name = item["folder_path"]
    app_type = "iot" if item.get("iot_enabled", False) else "non-iot"
    permissions = []

    # Extract permissions safely and remove trailing "/>"
    for permission in item.get("detected_permissions", []):
        split_permission = permission.split(".")
        if len(split_permission) >= 4:
            extracted_permission = split_permission[3].split('"')[0]
            permissions.append(extracted_permission)
    
    # Create the app entry with extracted information
    app_entry = {
        "app_name": app_name,
        "app_type": app_type,
        "permissions": permissions
    }
    
    app_data.append(app_entry)

pd.set_option('display.max_columns', None)

# Function to analyze app data
def analyze_app_data(app_data):
  categorized_data = []
  for app in app_data:
    app_type = app["app_type"]
    permissions = app["permissions"]
    existing_categories = {category: False for category in permission_categories.values()}
    for permission in permissions:
      if permission in permission_categories:
        existing_categories[permission_categories[permission]] = True
    categorized_data.append(
        {
            "app_name": app["app_name"],
            "app_type": app_type,
            "number_of_permissions": len(permissions),
            **existing_categories,
        }
    )
  return categorized_data

# Analyze app data
analyzed_data = analyze_app_data(app_data)

# Convert categorized data to Pandas DataFrame
df = pd.DataFrame(analyzed_data)

permission_stats = df.groupby('app_type')['number_of_permissions'].describe()

# # Print the DataFrame
# print(df)

print(permission_stats)

permission_counts = {}
categories = list(permission_categories.values())
categories_set = set(categories)  # Use set to remove duplicates

for app_type in ["iot", "non-iot"]:
    filtered_df = df[df['app_type'] == app_type]
    for category_name in categories_set:
        category_apps = filtered_df[(filtered_df[category_name] == True)]
        if category_name not in permission_counts:
            permission_counts[category_name] = {app_type: len(category_apps)}
        else:
            permission_counts[category_name][app_type] = len(category_apps)

# Plot data
plt.figure(figsize=(12, 6))
x_axis = range(len(categories_set))

colors = {"iot": "orange", "non-iot": "purple"}
bar_width = 0.4
offset = 0.2

for app_type, color in colors.items():
    y_axis = [permission_counts[category][app_type] for category in categories_set]
    plt.bar(
        [x + offset + (bar_width * (app_type == "iot")) for x in x_axis],
        y_axis,
        width=bar_width,
        label=app_type.upper(),
        color=color,
    )

plt.xticks(x_axis, categories_set, rotation=45, ha="right")
plt.xlabel("Permission Category")
plt.ylabel("Frequency")
plt.title("Frequency Distribution of Permissions for IoT and Non-IoT Apps")
plt.legend()
plt.tight_layout()
plt.show()

# Create separate DataFrames for IoT and non-IoT apps
df_iot = df[df["app_type"] == "iot"]
df_non_iot = df[df["app_type"] == "non-iot"]

# Perform two-tailed t-test
t_statistic, p_value = stats.ttest_ind(df_iot["number_of_permissions"], df_non_iot["number_of_permissions"])

# Print results
print("t-statistic:", t_statistic)
print("p-value:", p_value)

# Interpretation
if p_value < 0.05:
    print("Reject null hypothesis: IoT apps require significantly more permissions than non-IoT apps.")
else:
    print("Fail to reject null hypothesis: No significant difference found.")

def find_permission_cooccurrences(app_data):
  # Initialize dictionaries to store co-occurrence counts
  iot_cooccurrences = defaultdict(int)
  non_iot_cooccurrences = defaultdict(int)

  for app in app_data:
    app_type = app["app_type"]
    permissions = app["permissions"]

    # Identify co-occurring permissions
    for i in range(len(permissions)):
      for j in range(i + 1, len(permissions)):
        permission1 = permissions[i]
        permission2 = permissions[j]
        
        # Sort permission pair for consistent counting
        cooccurrence_pair = tuple(sorted((permission1, permission2)))
        
        if app_type == "iot":
          iot_cooccurrences[cooccurrence_pair] += 1
        else:
          non_iot_cooccurrences[cooccurrence_pair] += 1

  return iot_cooccurrences, non_iot_cooccurrences

# Analyze app data and find co-occurrences
iot_cooccurrences, non_iot_cooccurrences = find_permission_cooccurrences(app_data)

# Print co-occurrence counts
print("IoT Co-Occurrences:")
for permission_pair, count in iot_cooccurrences.items():
  print(f"\t{permission_pair}: {count}")

print("\nNon-IoT Co-Occurrences:")
for permission_pair, count in non_iot_cooccurrences.items():
  print(f"\t{permission_pair}: {count}")
