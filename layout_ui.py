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
        "Widgets and Views": set(),
        "Layout Types": set(),
        "Nested Layouts": set()
    }

    for file_path in layout_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                # Check for specific elements in the XML content
                if re.search(r'<TextView', line):
                    components["Widgets and Views"].add((file_path, line_number, "TextView"))
                if re.search(r'<Button', line):
                    components["Widgets and Views"].add((file_path, line_number, "Button"))
                
                # Check for layout types in the XML content
                if re.search(r'<LinearLayout', line):
                    components["Layout Types"].add(("LinearLayout", file_path))
                elif re.search(r'<RelativeLayout', line):
                    components["Layout Types"].add(("RelativeLayout", file_path))
                elif re.search(r'<ConstraintLayout', line):
                    components["Layout Types"].add(("ConstraintLayout", file_path))
                
                # Check for nested layouts in the XML content
                if re.search(r'</.*Layout>', line):
                    components["Nested Layouts"].add((file_path, line.strip()))

    return components

# Provide the path to your Android project folder
project_folder = 'FillUp'
layout_files = explore_layout_files(project_folder)
detected_components = analyze_layout_files(layout_files)

# Print categorized UI components including layout types and nested layouts
for category, components in detected_components.items():
    print(f"\n{category}:")
    if category in ["Nested Layouts", "Layout Types"]:
        for component in components:
            file_path, component_value = component
            print(f"File: {file_path}, {category[:-1]}: {component_value}")
    else:
        for component in components:
            file_path, line_number, component_name = component
            print(f"File: {file_path}, Line {line_number}: Detected {component_name}")
