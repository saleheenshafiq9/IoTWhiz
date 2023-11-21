from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api_usage import detect_api_usage
from dynamic_code_loading import detect_dynamic_code_loading
from permission_pattern import detect_permissions
from layout_ui import explore_layout_files, analyze_layout_files
from jadx import decompile_apk

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
    detected_components = analyze_layout_files(layout_files)

    # Return the analyzed components back to the frontend or perform further processing
    return detected_components

@app.post("/upload-apk/")
async def upload_apk(apk_file: APKFile):
    file_name = apk_file.file_name
    decompile_apk(file_name,'source_codes')
    return {"file_name": file_name, "message": "APK file name received successfully"}