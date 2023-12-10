import requests
import os
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

client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['iotWhiz']  # Replace with your database name

url = "https://androzoo.uni.lu/api/download"
apikey = "36b0de1dba01073d4a53a50d2060e79a0efc33337e95b3d7b7a448f7f6665e4e"
sha256_list = [
    "00F960BCC0067F26D8FDF229678B19CE79B1D984AE78454FE5441B24E984FE75",
    "00F965A0D3712E849F0487C9BF347E6C53F4A1DDB8B750D81908D16993F5D14F",
    "00F966DF173CB11C2F227D3DBF639F5454E4E923AB3023AEA154AA04C8C1E35D",
    "00F96F73F7799E0CFE8A851C98C86B3F67B3ED3E7543524A236968E3EDA3929B",
    "00F9716A878996842BBC366274B4A5FF7EC6078E53311B98752A3743FA9D1CC7",
    "00F97311438FCB84B82089B53B4B57E86ECE737FB4983273C8EADA54578EA1FD",
    "00F974AA8F3CCDB82BBEBAB6A4C982F9556B44956ECAE8427CAFB7B3AC01965D",
    "00F9767160DE21506E5A69724A0DF717CC9C84E145B19F998A23CC1BDF63A7D5",
    "00F9796923D8FEAC55F7B3632822462212CECED9AC08C78CDE665368F85E84DA",
    "00F97E4AA6508CFA697C27872FC22B41F7E1633E33A96B73726C06C510573199",
    "00F9803D0600B4325C08E0A753A8F000FEB388A0DCA9ABABB993DF0188CD74E0",
    "00F984407339048425F5C5CA2EBDA3ABE818B58469680E4EF233BE5B44F1D17A",
    "00F988DAC939557112E0FB91A5C6B710C882FFB74936A3803274CC10DF236CCE"
]


for sha256 in sha256_list:
    filename, filesize = download_apk(apikey, sha256)
    data_to_store = {
        "file_name": filename,
        "file_size": filesize,
    }

    store_data_in_mongodb("downloads", filename, data_to_store)
    output_dir = decompile_apk(filename)
    print(output_dir + "successful decompilation")

    received_folder_path = filename.replace(".apk", "")
    received_folder_path_loc = os.path.join('..', received_folder_path)
    received_iot_enabled = False

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




