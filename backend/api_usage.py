import os
import re

def detect_api_usage(folder_path):
    api_calls = set()
    total_api_usages = 0

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            try:
                if file_name.endswith('.java'):
                    file_path = os.path.join(root, file_name)
                    relative_path = os.path.relpath(file_path, folder_path)
                    with open(file_path, 'r', errors='ignore') as file:
                        lines = file.readlines()
                        line_number = 0
                        for line in lines:
                            line_number += 1
                            content = line.strip()
                            # Define regex patterns to match API-related code
                            api_patterns = [
                                r'(HttpURLConnection|OkHttp|HttpClient|RestTemplate)\\.',
                                r'new\s+URL\(',
                                r'JSONObject|JSONArray',
                                # Add more patterns for different API usage
                            ]
                            for pattern in api_patterns:
                                matches = re.findall(pattern, content)
                                if matches:
                                    api_calls.add(f"{relative_path}:{line_number}: {content}")
                                    total_api_usages += len(matches)
            except Exception as e:
                print(f"Error processing file: {file_name}. Skipping. Error: {e}")

    return api_calls, total_api_usages