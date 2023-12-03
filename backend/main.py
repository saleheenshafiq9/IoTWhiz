from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app = FastAPI()

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

class APKFile(BaseModel):
    file_name: str

class APIKeySHA256(BaseModel):
    api_key: str
    sha256: str

@app.post("/upload-folder/")
async def upload_folder(folder_path: FolderPath):
    received_folder_path = folder_path.folder_path

    # Use the received folder path in the detect_api_usage function
    detected_apis, total_usages = detect_api_usage(received_folder_path)
    detected_dynamic_loading, total_dynamic_usages = detect_dynamic_code_loading(received_folder_path)
    detected_permissions, total_permissions = detect_permissions(received_folder_path)

    # You can return the results back to the frontend or perform further processing
    return {"detected_apis": list(detected_apis), "total_usages": total_usages, "detected_dynamic_loading": list(detected_dynamic_loading), "total_dynamic_usages": total_dynamic_usages, "detected_permissions": list(detected_permissions), "total_permissions": total_permissions}

@app.post("/analyze-layout/")
async def analyze_layout(folder_path: FolderPath):
    received_folder_path = folder_path.folder_path

    # Use the received folder path in the explore_layout_files function
    layout_files = explore_layout_files(received_folder_path)

    # Use the layout files to analyze UI components with analyze_layout_files function
    detected_components = analyze_layout_files(layout_files, received_folder_path)

    # Return the analyzed components back to the frontend or perform further processing
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

    filename = download_apk(received_api_key, received_sha256)
    
    return {
        "message": "API Key and SHA256 received successfully",
        "received_api_key": received_api_key,
        "received_sha256": received_sha256,
        "download_file": filename
    }

@app.post("/receive-api-key-sha256-get-source-code/")
async def receive_api_key_sha256(api_key_sha256: APIKeySHA256):
    received_api_key = api_key_sha256.api_key
    received_sha256 = api_key_sha256.sha256

    print("Invoked /receive-api-key-sha256-get-source-code/")

    filename = download_apk(received_api_key, received_sha256)
    output_dir = decompile_apk(filename)

    response_data = {
        "message": "API Key and SHA256 received successfully",
        "received_api_key": received_api_key,
        "received_sha256": received_sha256,
        "download_file": filename,
        "output_directory": output_dir,
    }
    
    return response_data

@app.post("/loc-class-method/")
async def upload_folder(folder_path: FolderPath):
    received_folder_path = folder_path.folder_path

    lines_of_code, skipped_files = count_lines_of_code(received_folder_path)
    classes, methods = count_classes_methods(received_folder_path)

    return {
            'lines_of_code': lines_of_code,
            'number_of_classes': classes,
            'number_of_methods': methods,
        }

@app.post("/database-storage/")
async def upload_folder(folder_path: FolderPath):
    received_folder_path = folder_path.folder_path
    strategies_found = search_database_related_strategies(received_folder_path)
    strategies_description = describe_database_strategies(strategies_found, received_folder_path)

    return strategies_description

@app.post("/reflection/")
async def upload_folder(folder_path: FolderPath):
    received_folder_path = folder_path.folder_path

    reflections_summary = search_for_patterns(received_folder_path)
    
    return reflections_summary