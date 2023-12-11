from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pymongo import MongoClient
from pydantic import BaseModel
from api_usage import detect_api_usage
from dynamic_code_loading import detect_dynamic_code_loading
from permission_pattern import detect_permissions
from layout_ui import explore_layout_files, analyze_layout_files
from jadx import decompile_apk
from APK_download import download_apk
from count_lines import count_lines_of_code
from count_classes import count_classes_methods
from database_storage import search_database_related_strategies, describe_database_strategies
from reflection import search_for_patterns
from api_analysis import calculate_stats
from dc_analysis import calculate_dynamic_stats
from pp_analysis import calculate_permissions, calculate_cooccurrences, CooccurrenceError, get_permission_counts
import os
from typing import Dict

app = FastAPI()

client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['iotWhiz']  # Replace with your database name

# CORS settings to allow requests from your React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FolderPath(BaseModel):
    folder_path: str
    iot_enabled: bool 


class APKFile(BaseModel):
    file_name: str

class APIKeySHA256(BaseModel):
    api_key: str
    sha256: str

def store_data_in_mongodb(collection_name, folder_path, data):
    collection = db[collection_name]
    existing_data = collection.find_one({"folder_path": folder_path})

    if existing_data:
        # Update existing document if the folder path already exists
        collection.update_one({"folder_path": folder_path}, {"$set": data})
    else:
        # Insert new document if the folder path doesn't exist
        data["folder_path"] = folder_path
        collection.insert_one(data)

@app.post("/upload-folder/")
async def upload_folder(folder_path: FolderPath):
    received_folder_path = folder_path.folder_path
    received_iot_enabled = folder_path.iot_enabled

    # Use the received folder path in the detect_api_usage function
    detected_apis, total_usages = detect_api_usage(received_folder_path)
    detected_dynamic_loading, total_dynamic_usages = detect_dynamic_code_loading(received_folder_path)
    detected_permissions, total_permissions = detect_permissions(received_folder_path)

    data_to_store = {
        "detected_apis": list(detected_apis),
        "total_usages": total_usages,
        "detected_dynamic_loading": list(detected_dynamic_loading),
        "total_dynamic_usages": total_dynamic_usages,
        "detected_permissions": list(detected_permissions),
        "total_permissions": total_permissions,
        "folder_path": received_folder_path,
        'iot_enabled': received_iot_enabled,

    }

    store_data_in_mongodb("upload_folder_data", received_folder_path, data_to_store)

    return {
        "detected_apis": list(detected_apis),
        "total_usages": total_usages,
        "detected_dynamic_loading": list(detected_dynamic_loading),
        "total_dynamic_usages": total_dynamic_usages,
        "detected_permissions": list(detected_permissions),
        "total_permissions": total_permissions,
    }

@app.post("/analyze-layout/")
async def analyze_layout(folder_path: FolderPath):
    received_folder_path = folder_path.folder_path
    received_iot_enabled = folder_path.iot_enabled

    layout_files = explore_layout_files(received_folder_path)
    detected_components = analyze_layout_files(layout_files, received_folder_path)

    # Convert set to list before storing in MongoDB
    detected_components_list = list(detected_components)

    # Store the data in MongoDB
    data_to_store = {
        "detected_components": detected_components_list,
        "folder_path": received_folder_path,
        'iot_enabled': received_iot_enabled,

    }
    store_data_in_mongodb("analyze_layout_data", received_folder_path, data_to_store)

    return detected_components


@app.post("/upload-apk/")
async def upload_apk(apk_file: APKFile):
    file_name = apk_file.file_name
    output_dir = decompile_apk(file_name)
    return {"file_name": file_name, "message": "APK file name received successfully", "output_directory": output_dir}

@app.post("/receive-api-key-sha256/")
async def receive_api_key_sha256(api_key_sha256: APIKeySHA256):
    received_api_key = api_key_sha256.api_key
    received_sha256 = api_key_sha256.sha256

    print("Invoked /receive-api-key-sha256/")

    filename, file_size = download_apk(received_api_key, received_sha256)

    data_to_store = {
        "file_name": filename,
        "file_size": file_size,
    }
    store_data_in_mongodb("downloads", filename, data_to_store)
    
    return {
        "message": "API Key and SHA256 received successfully",
        "received_api_key": received_api_key,
        "received_sha256": received_sha256,
        "download_file": filename,
        "file_size": file_size
    }

@app.post("/receive-api-key-sha256-get-source-code/")
async def receive_api_key_sha256(api_key_sha256: APIKeySHA256):
    received_api_key = api_key_sha256.api_key
    received_sha256 = api_key_sha256.sha256

    print("Invoked /receive-api-key-sha256-get-source-code/")

    filename, file_size = download_apk(received_api_key, received_sha256)
    output_dir = decompile_apk(filename)

    data_to_store = {
        "file_name": filename,
        "file_size": file_size,
    }
    store_data_in_mongodb("downloads", filename, data_to_store)

    response_data = {
        "message": "API Key and SHA256 received successfully",
        "received_api_key": received_api_key,
        "received_sha256": received_sha256,
        "download_file": filename,
        "output_directory": output_dir,
        "file_size": file_size
    }
    
    return response_data

@app.post("/loc-class-method/")
async def upload_folder(folder_path: FolderPath):
    received_folder_path = folder_path.folder_path
    received_iot_enabled = folder_path.iot_enabled

    lines_of_code, skipped_files = count_lines_of_code(received_folder_path)
    classes, methods = count_classes_methods(received_folder_path)

    # Store the data in MongoDB
    data_to_store = {
        'lines_of_code': lines_of_code,
        'number_of_classes': classes,
        'number_of_methods': methods,
        'iot_enabled': received_iot_enabled,
        'folder_path': received_folder_path,
    }
    store_data_in_mongodb("loc_class_method_data", received_folder_path, data_to_store)

    return {
        'lines_of_code': lines_of_code,
        'number_of_classes': classes,
        'number_of_methods': methods,
        'iot_enabled': received_iot_enabled,
        'folder_path': received_folder_path,
    }

@app.post("/database-storage/")
async def upload_folder(folder_path: FolderPath):
    received_folder_path = folder_path.folder_path
    received_iot_enabled = folder_path.iot_enabled
    strategies_found = search_database_related_strategies(received_folder_path)
    strategies_description = describe_database_strategies(strategies_found, received_folder_path)

    # Store the data in MongoDB
    data_to_store = {
        "strategies_found": strategies_found,
        "strategies_description": strategies_description,
        "folder_path": received_folder_path,
        'iot_enabled': received_iot_enabled,
    }
    store_data_in_mongodb("database_storage_data", received_folder_path, data_to_store)

    return strategies_description

@app.post("/reflection/")
async def upload_folder(folder_path: FolderPath):
    received_folder_path = folder_path.folder_path
    received_iot_enabled = folder_path.iot_enabled

    reflections_summary = search_for_patterns(received_folder_path)
    
    # Store the data in MongoDB
    data_to_store = {
        "reflections_summary": reflections_summary,
        "folder_path": received_folder_path,
        'iot_enabled': received_iot_enabled,

    }
    store_data_in_mongodb("reflection_data", received_folder_path, data_to_store)

    return reflections_summary

@app.get("/stats")
async def get_statistics():
    try:
        stats_data = calculate_stats()
        return JSONResponse(content=stats_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/histogram")
async def get_histogram_image():
    # Define the relative path to the public directory from the backend directory
    relative_path = os.path.join('..', 'iotwhiz', 'public', 'histogram.png')

    # Return the image file using FileResponse
    return FileResponse(relative_path)

@app.get("/dynamic_stats")
async def get_dynamic_stats():
    try:
        stats_data = calculate_dynamic_stats()
        print(stats_data)
        return JSONResponse(content=stats_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/permission_stats")
async def get_permisson_stats():
    try:
        stats_data = calculate_permissions()
        return JSONResponse(content=stats_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@app.get('/permission_cooccurrences', response_model=Dict[str, Dict[str, int]])
async def get_cooccurrences():
    try:
        cooccurrences = calculate_cooccurrences()
        return cooccurrences
    except CooccurrenceError as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/permission-counts")
async def get_permission_counts_api():
    try:
        results = get_permission_counts()
        print(results)  # Output the results to console for debugging purposes
        return results  # Return the permission counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating permission counts: {e}")