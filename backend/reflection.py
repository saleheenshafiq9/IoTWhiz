import re
import os
import json

def search_for_patterns(project_folder_name):
    current_directory = os.getcwd()
    project_folder = os.path.join(current_directory, project_folder_name)

    reflection_patterns = {
        'Class_Loading': [],
        'Method_Retrieval': [],
        'Instance_Creation': [],
        'Method_Invocation': [],
        'Field_Retrieval': [],
        'Access_Control': [],
        'Annotations_Retrieval': []
    }

    total_reflection_count = 0

    for root, _, files in os.walk(project_folder):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                except OSError as e:
                    print(f"Skipping file: {file_path} due to error: {e}")
                    continue

                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()

                for reflection_type in reflection_patterns:
                    pattern = get_pattern(reflection_type)
                    matches = re.finditer(pattern, file_content)
                    for match in matches:
                        line_num = get_line_number(lines, match.start())
                        reflection_patterns[reflection_type].append({
                            'file_path': file_path.replace(project_folder, ''),
                            'line_number': line_num,
                            'line_content': lines[line_num - 1].strip()
                        })
                        total_reflection_count += 1

    reflection_counts = {
        reflection_type: {
            'count': len(occurrences),
            'occurrences': occurrences
        } for reflection_type, occurrences in reflection_patterns.items()
    }

    reflection_counts['Total_Reflections'] = total_reflection_count
    return reflection_counts

def get_pattern(reflection_type):
    patterns = {
        'Class_Loading': r'\bClass\.forName\b',
        'Method_Retrieval': r'\b(getMethod|getDeclaredMethod)\b',
        'Instance_Creation': r'\bnewInstance\b',
        'Method_Invocation': r'\binvoke\b',
        'Field_Retrieval': r'\bgetDeclaredFields\b',
        'Access_Control': r'\bsetAccessible\(true\)\b',
        'Annotations_Retrieval': r'\bgetDeclaredAnnotations\b'
    }
    return patterns.get(reflection_type, '')

def get_line_number(lines, index):
    line_num = 1
    for line in lines:
        if index <= len(line):
            return line_num
        index -= len(line)
        line_num += 1
    return -1
