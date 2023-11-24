import os
import re

def count_classes_methods(project_folder):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.join(current_directory, project_folder)

    class_pattern = re.compile(r'\bclass\s+([A-Za-z0-9_]+)\s*[{]?')
    method_pattern = re.compile(r'\b([A-Za-z0-9_]+)\s+([A-Za-z0-9_]+)\s*\([^)]*\)\s*[{]?')

    class_count = 0
    method_count = 0

    for root, dirs, files in os.walk(project_path):
        for file_name in files:
            if file_name.endswith(".java"):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r') as file:
                        content = file.read()
                        classes = class_pattern.findall(content)
                        methods = method_pattern.findall(content)
                        class_count += len(classes)
                        method_count += len(methods)
                except Exception as e:
                    print(f"Error parsing file {file_path}: {e}")

    return class_count, method_count

# Provide the relative path to your Android project folder
project_relative_path = 'Pizza-Shop-Refactored'
classes, methods = count_classes_methods(project_relative_path)
print(f"Number of classes: {classes}")
print(f"Number of methods: {methods}")
