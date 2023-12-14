import requests
import os
import csv
from APK_download import download_apk
from main import store_data_in_mongodb
from jadx import decompile_apk
from pymongo import MongoClient
from api_usage import detect_api_usage
from dynamic_code_loading import detect_dynamic_code_loading
from permission_pattern import detect_permissions
from layout_ui import explore_layout_files, analyze_layout_files
from count_lines import count_lines_of_code
from count_classes import count_classes_methods
from database_storage import search_database_related_strategies, describe_database_strategies
from reflection import search_for_patterns

url = "https://androzoo.uni.lu/api/download"
apikey = "36b0de1dba01073d4a53a50d2060e79a0efc33337e95b3d7b7a448f7f6665e4e"

def analyze_apk():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_directory, 'data.csv')

    client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
    db = client['iotWhiz_new']  # Replace with your database name

    with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header row

            for row in csv_reader:
                print(row)
                sha256 = row[0]  # Assuming SHA256 is in the first column
                received_iot_enabled = int(row[1])  # Assuming status is in the second column as 0 or 1

                filename, filesize = download_apk(apikey, sha256)

                output_dir = decompile_apk(filename)
                print(output_dir + "successful decompilation")

                received_folder_path = filename.replace(".apk", "")
                received_folder_path_loc = os.path.join('..', received_folder_path)
                received_iot_enabled = bool(received_iot_enabled)

                data_to_store = {
                    "folder_path": received_folder_path,
                    "apk_size": filesize,
                    "iot_enabled": received_iot_enabled
                }

                store_data_in_mongodb("downloads", received_folder_path, data_to_store)
                # Use the received folder path in the detect_api_usage function
                detected_apis, total_usages = detect_api_usage(received_folder_path)
                detected_dynamic_loading, total_dynamic_usages = detect_dynamic_code_loading(received_folder_path)
                detected_permissions, total_permissions = detect_permissions(received_folder_path)

                data_to_store_api_usages = {
                    "detected_apis": list(detected_apis),
                    "total_usages": total_usages,
                    "detected_dynamic_loading": list(detected_dynamic_loading),
                    "total_dynamic_usages": total_dynamic_usages,
                    "detected_permissions": list(detected_permissions),
                    "total_permissions": total_permissions,
                    "folder_path": received_folder_path,
                    'iot_enabled': received_iot_enabled,
                }

                store_data_in_mongodb("upload_folder_data", received_folder_path, data_to_store_api_usages)

                layout_files = explore_layout_files(received_folder_path)
                detected_components = analyze_layout_files(layout_files, received_folder_path)

                # Convert set to list before storing in MongoDB
                detected_components_list = list(detected_components)

                # Store the data in MongoDB
                data_to_store_layout = {
                    "detected_components": detected_components_list,
                    "folder_path": received_folder_path,
                    'iot_enabled': received_iot_enabled,

                }
                store_data_in_mongodb("analyze_layout_data", received_folder_path, data_to_store_layout)

                lines_of_code, skipped_files = count_lines_of_code(received_folder_path_loc)
                classes, methods = count_classes_methods(received_folder_path_loc)

                # Store the data in MongoDB
                data_to_store_count = {
                    'lines_of_code': lines_of_code,
                    'number_of_classes': classes,
                    'number_of_methods': methods,
                    'iot_enabled': received_iot_enabled,
                    'folder_path': received_folder_path,
                }
                store_data_in_mongodb("loc_class_method_data", received_folder_path, data_to_store_count)

                strategies_found = search_database_related_strategies(received_folder_path)
                strategies_description = describe_database_strategies(strategies_found, received_folder_path)

                # Store the data in MongoDB
                data_to_store_db = {
                    "strategies_found": strategies_found,
                    "strategies_description": strategies_description,
                    "folder_path": received_folder_path,
                    'iot_enabled': received_iot_enabled,
                }
                store_data_in_mongodb("database_storage_data", received_folder_path, data_to_store_db)

                reflections_summary = search_for_patterns(received_folder_path)
                
                # Store the data in MongoDB
                data_to_store_ref = {
                    "reflections_summary": reflections_summary,
                    "folder_path": received_folder_path,
                    'iot_enabled': received_iot_enabled,

                }
                store_data_in_mongodb("reflection_data", received_folder_path, data_to_store_ref)

analyze_apk()