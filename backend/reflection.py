import re
import os
import json

def search_for_patterns(project_folder_name):
    current_directory = os.getcwd()
    project_folder = os.path.join(current_directory, project_folder_name)

    reflection_patterns = {
        'Class Loading': r'\bClass\.forName\b',
        'Method Retrieval': r'\b(getMethod|getDeclaredMethod)\b',
        'Instance Creation': r'\bnewInstance\b',
        'Method Invocation': r'\binvoke\b',
        'Field Retrieval': r'\bgetDeclaredFields\b',
        'Access Control': r'\bsetAccessible\(true\)\b',
        'Annotations Retrieval': r'\bgetDeclaredAnnotations\b'
    }

    reflection_counts = {reflection_type: {'count': 0, 'occurrences': []} for reflection_type in reflection_patterns}

    total_reflection_count = 0

    for root, _, files in os.walk(project_folder):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()
                except OSError as e:
                    print(f"Skipping file: {file_path} due to error: {e}")
                    continue

                for reflection_type, pattern in reflection_patterns.items():
                    matches = re.findall(pattern, file_content)
                    count = len(matches)
                    reflection_counts[reflection_type]['count'] += count
                    total_reflection_count += count

                    if count > 0:
                        reflection_counts[reflection_type]['occurrences'].append(file_path)

    reflection_counts['Total Reflections'] = total_reflection_count
    return reflection_counts

# if __name__ == "__main__":
#     project_folder_name = 'backend/C94B84568949584210FFEA778B6E81F40888EC26CBAE4FC4289D809D9E24ADD1'
#     reflections_summary = search_for_patterns(project_folder_name)
#     print(reflections_summary)
