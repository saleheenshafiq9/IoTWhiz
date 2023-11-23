import os
import re

def detect_permissions(folder_path):
    permission_lines = set()
    total_permissions = 0
    parent_folder = "goodtime"  # Replace 'goodtime' with the actual parent folder name to be removed

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
                            # Removing the parent folder name while retaining the subfolder structure
                            relative_path = os.path.relpath(manifest_file, parent_folder)
                            permission_lines.add(f"{relative_path}:{line_number}: {line.strip()}")
                            total_permissions += len(matches)

    return permission_lines, total_permissions
