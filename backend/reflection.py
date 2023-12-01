import re
import os

def search_for_patterns(project_folder_name):
    current_directory = os.getcwd()
    project_folder = os.path.join(current_directory, project_folder_name)

    for root, _, files in os.walk(project_folder):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                except OSError as e:
                    print(f"Skipping file: {file_path} due to error: {e}")
                    continue

                patterns = [
                    r'\bClass\.forName\b',
                    r'\bgetMethod\b',
                    r'\bgetDeclaredMethod\b',
                    r'\bnewInstance\b',
                    r'\binvoke\b',
                    r'\bgetDeclaredFields\b',
                    r'\bsetAccessible\(true\)\b',
                    r'\bgetDeclaredAnnotations\b'
                ]

                for pattern in patterns:
                    matches = re.finditer(pattern, file_content)
                    for match in matches:
                        line_number = match.start() + 1  # Convert index to line number
                        line = file_content[match.start():match.end()]
                        print(f"File: {file_path}")
                        print(f"Line {line_number}: {line}")

if __name__ == "__main__":
    project_folder_name = 'backend/goodtime'
    search_for_patterns(project_folder_name)
