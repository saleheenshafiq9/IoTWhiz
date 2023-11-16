import os
import re

def detect_permissions(folder_path):
    permission_lines = set()
    total_permissions = 0

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name == 'AndroidManifest.xml':
                manifest_file = os.path.join(root, file_name)
                with open(manifest_file, 'r') as file:
                    lines = file.readlines()
                    for line_number, line in enumerate(lines, start=1):
                        # Define regex pattern to match permission-related lines
                        permission_pattern = r'<uses-permission\s+android:name="android\.permission\.\w+"'
                        matches = re.findall(permission_pattern, line)
                        if matches:
                            permission_lines.add(f"{manifest_file}:{line_number}: {line.strip()}")
                            total_permissions += len(matches)

    return permission_lines, total_permissions

# Provide the path to your Android project folder
project_folder = 'goodtime'
detected_permissions, total_permissions = detect_permissions(project_folder)
print("Detected permissions:")
for permission_line in detected_permissions:
    print(permission_line)

print(f"Total permissions found: {total_permissions}")
