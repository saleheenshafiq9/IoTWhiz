import os
import re

def explore_layout_files(folder_path):
    layout_files = []
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.xml'):
                file_path = os.path.join(root, file_name)
                layout_files.append(file_path)
    return layout_files

def analyze_layout_files(layout_files):
    components = {
        "Widgets_and_Views": set(),
        "Layout_Types": set(),
        "Nested_Layouts": set()
    }

    parent_folder = "goodtime"  # Replace 'goodtime' with the actual parent folder name to be removed

    for file_path in layout_files:
        # Removing the parent folder name while retaining the subfolder structure
        relative_path = os.path.relpath(file_path, parent_folder)
        file_name_only = os.path.basename(file_path)  # Extracting only the file name
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                # Check for specific elements in the XML content
                if re.search(r'<TextView', line):
                    components["Widgets_and_Views"].add((relative_path, line_number, "TextView"))
                if re.search(r'<Button', line):
                    components["Widgets_and_Views"].add((relative_path, line_number, "Button"))
                
                # Check for layout types in the XML content
                if re.search(r'<LinearLayout', line):
                    components["Layout_Types"].add(("LinearLayout", relative_path))
                elif re.search(r'<RelativeLayout', line):
                    components["Layout_Types"].add(("RelativeLayout", relative_path))
                elif re.search(r'<ConstraintLayout', line):
                    components["Layout_Types"].add(("ConstraintLayout", relative_path))
                
                # Check for nested layouts in the XML content
                if re.search(r'</.*Layout>', line):
                    components["Nested_Layouts"].add((relative_path, line.strip()))

    return components
