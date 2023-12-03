import os

def count_lines_of_code(folder_path):
    total_lines = 0
    skipped_files = []

    current_directory = os.path.dirname(__file__)  # Get the current directory of the script
    project_folder = os.path.join(current_directory, folder_path)

    for root, _, files in os.walk(project_folder):
        for file_name in files:
            if file_name.endswith('.java'):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Ignore empty lines and lines containing only whitespace
                            if line.strip() == '' or line.isspace():
                                continue
                            # Ignore single-line comments
                            if line.strip().startswith('//'):
                                continue
                            # Ignore multi-line comments
                            if line.strip().startswith('/*'):
                                continue
                            if line.strip().endswith('*/'):
                                continue
                            total_lines += 1
                except Exception as e:
                    skipped_files.append(file_path)
                    print(f"Skipped file due to error: {file_path} - Error: {str(e)}")

    return total_lines, skipped_files

# Provide the specific path to your Android project folder containing Java source files
# project_folder = 'goodtime'
# total_lines, skipped_files = count_lines_of_code(project_folder)
# print(f"Total lines of code: {total_lines}")
# print(f"Skipped files: {skipped_files}")
