import os
import re

def detect_dynamic_code_loading(folder_path):
    dynamic_loading_lines = set()
    total_dynamic_usages = 0

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            try:
                if file_name.endswith('.java'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', errors='ignore') as file:
                        lines = file.readlines()
                        for line_number, line in enumerate(lines, start=1):
                            # Updated regex pattern to match different forms of DexClassLoader instantiation
                            dynamic_loading_pattern = r'(ClassLoader|DexClassLoader)\s*\(\s*.*\s*,\s*.*\s*,\s*.*\s*\)'
                            matches = re.findall(dynamic_loading_pattern, line)
                            if matches:
                                # Extracting only the file name from the full file path
                                file_name_only = os.path.basename(file_path)
                                dynamic_loading_lines.add(f"{file_name_only}:{line_number}: {line.strip()}")
                                total_dynamic_usages += len(matches)
            except Exception as e:
                print(f"Error processing file: {file_name}. Skipping. Error: {e}")

    return dynamic_loading_lines, total_dynamic_usages
