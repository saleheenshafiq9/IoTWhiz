import pdfkit
from api_analysis import calculate_stats
from dc_analysis import calculate_dynamic_stats
from pp_analysis import calculate_permissions, get_permission_counts
from lcm_analysis import calculate_lcm, lcm_inferential
from dbs_analysis import get_database_strategy_percentages
from reflect_analysis import calculate_reflections
import os

# Set the path to wkhtmltopdf binary
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

def generate_pdf_from_stats():
    stats_data = calculate_stats()
    stats_data_dynamic = calculate_dynamic_stats()
    stats_data_permissions = calculate_permissions()
    permission_counts_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'permission_top10.png')
    results = get_permission_counts()
    stats_lcm = calculate_lcm()
    lcm_inf = lcm_inferential()
    db_percentage = get_database_strategy_percentages()
    reflections = calculate_reflections()
    desc_ref_data = reflections["descriptive_results"]

    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Function to create HTML content for stats data
    def create_html_content(data):
        content = ""
        for key, value in data.items():
            if isinstance(key, tuple):  # Checking if the key is a tuple
            # Convert the tuple to a string and replace underscores with spaces
                display_key = ' '.join(map(str, key)).replace('_', ' ').title()
            else:
                display_key = key.replace('_', ' ').title()
            if key == 'Histogram' or key == 'distribution_path':
                if key == 'distribution_path':
                    content += "<div style='page-break-before: always;'></div>"
                image_filename = os.path.basename(value)
                # If the key is 'Histogram', embed the image using its path
                image_path = os.path.join(current_directory, image_filename)
                image_tag = f"<div style='text-align:center'><img src='{image_path}' style='max-width:100%; height:auto;'></div>"
                content += f"<h2>{display_key}</h2>"
                content += image_tag
            else:
                content += f"<h2>{display_key}</h2>"
                content += f"<p style='margin-bottom:20px;font-size:20px;text-align: justify;'>{value}</p>"

        return content

    # Create HTML content for both sets of data
    city_image_path = os.path.join(current_directory, 'city.png')
    city_image_tag = f"<div style='text-align:center;margin-bottom:40px;margin-top:60px'><img src='{city_image_path}' style='width:50%; height:auto;'></div>"    
    logo_image_path = os.path.join(current_directory, 'logo.png')
    logo_image_tag = f"<div style='text-align:center;background-color:#0056b3;margin-bottom:40px;margin-top:60px'><img src='{logo_image_path}' style='width:40%; height:auto;'></div>"
    html_content = city_image_tag
    html_content += logo_image_tag
    html_content += "<h1 style='text-align:center;margin-top:80px;color:#0056b3'>IoTWhiz Report</h1>"

    html_content += "<h1 style='text-align:center;margin-top:80px;'>A Comprehensive Analysis Tool for IoT and Non-IoT Android Apps</h1>"
    html_content += "<h3 style='text-align:center'>Discover distinctive characteristics using API usage, permissions, UI layouts, code size, and more.</h3>"
    html_content += "<h3 style='text-align:center'>Visualizations unveil app differences, guiding efficient development choices.</h3>"
    html_content += "<div style='page-break-before: always;'></div>"
    html_content += "<h2 style='text-align:center'>API Usage Comparison </h2>"
    html_content += create_html_content(stats_data)
    html_content += "<div style='page-break-before: always;'></div>"
    html_content += "<h2 style='text-align:center'>Dynamic Class Usage Comparison </h2>"
    html_content += create_html_content(stats_data_dynamic)
    html_content += "<div style='page-break-before: always;'></div>"
    html_content += "<h2 style='text-align:center'>App Permissions Comparison </h2>"
    html_content += create_html_content(stats_data_permissions)
    html_content += f"<h3>Top 10 Permission Co-occurrences</h3>"
    permission_image_tag = f"<img src='{permission_counts_image_path}' style='max-width:100%; height:auto;'>"
    html_content += permission_image_tag
    html_content += create_html_content(results)

    def format_dataframe_statistics(dataframe):
        statistics = dataframe.describe().transpose()
        formatted_stats = {}
        for index, row in statistics.iterrows():
            formatted_stats[index] = {
                "count": row["count"],
                "mean": row["mean"],
                "std": row["std"],
                "min": row["min"],
                "25%": row["25%"],
                "50%": row["50%"],
                "75%": row["75%"],
                "max": row["max"]
            }
        return formatted_stats

    # Extract statistics for 'iot_data_numeric' and 'non_iot_data'
    iot_data_stats = format_dataframe_statistics(stats_lcm['iot_data_numeric'])
    non_iot_data_stats = format_dataframe_statistics(stats_lcm['non_iot_data'])
    html_content += "<h2 style='text-align:center'>Code Length Comparison </h2>"

    html_content += create_html_content({"iot_data_numeric": iot_data_stats})
    html_content += create_html_content({"non_iot_data": non_iot_data_stats})

    html_content += "<h2>Correlation Matrix (IoT)</h2>"
    html_content += "<table border='1'><tr><th></th>"

    columns = list(lcm_inf['iot_correlation_matrix'].keys())
    for col in columns:
        html_content += f"<th>{col}</th>"
    html_content += "</tr>"
    for col in columns:
        html_content += f"<tr><th>{col}</th>"
        for inner_col in columns:
            html_content += f"<td>{lcm_inf['iot_correlation_matrix'][col][inner_col]}</td>"
        html_content += "</tr>"
    html_content += "</table>"

    html_content += "<h2>Correlation Matrix (Non-IoT)</h2>"
    html_content += "<table border='1'><tr><th></th>"
    columns = list(lcm_inf['non_iot_correlation_matrix'].keys())
    for col in columns:
        html_content += f"<th>{col}</th>"
    html_content += "</tr>"
    for col in columns:
        html_content += f"<tr><th>{col}</th>"
        for inner_col in columns:
            html_content += f"<td>{lcm_inf['non_iot_correlation_matrix'][col][inner_col]}</td>"
        html_content += "</tr>"
    html_content += "</table>"
    html_content += "<div style='page-break-before: always;'></div>"

    # Display boxplots horizontally
    html_content += "<h2>Boxplots (IoT vs Non-IoT)</h2>"
    html_content += "<div style='display:flex;'>"
    for path in lcm_inf['boxplot_paths']:
        image_filename = os.path.basename(path)
        image_path = os.path.join(current_directory, image_filename)
        html_content += f"<img src='{image_path}' style='width:30%; padding:5px;'>"
    html_content += "</div>"

    # Display scatterplots vertically
    html_content += "<h2>Scatterplots (IoT vs Non-IoT)</h2>"
    for path in lcm_inf['scatterplot_paths']:
        image_filename = os.path.basename(path)
        image_path = os.path.join(current_directory, image_filename)
        html_content += f"<img src='{image_path}' style='width:30%; height:auto; margin-bottom:20px;'>"

    def create_html_table(data, title=None):
        html_content = ""
        if title:
            html_content += f"<h2>{title}</h2>"
        html_content += "<table border='1'>"
        for key, values in data.items():
            html_content += "<tr>"
            html_content += f"<th>{key}</th>"
            for item in values:
                # Check if the item is numeric and format it accordingly
                if isinstance(values[item], (int, float)):
                    html_content += f"<td>{values[item]:.4f}</td>"  # Adjust the formatting as needed
                else:
                    html_content += f"<td>{values[item]}</td>"
            html_content += "</tr>"
        html_content += "</table>"
        return html_content

    html_content += "<div style='page-break-before: always;'></div>"
    html_content += "<h2 style='text-align:center'>Database Storage Comparison </h2>"
    db_percentage_table = create_html_table(db_percentage['database_strategy_percentages'], "Database Strategy Percentages")
    t_test_table = create_html_table(db_percentage['statistical_test_results'], "T-Test Results")
    chi_square_table = create_html_table(db_percentage['chi_test_results'], "Chi-Square Test Results")
    corr_matrix_table = create_html_table(db_percentage['corr_analysis'], "Correlation Matrix")
    test_results_table = f"<div style='display:flex;'>{t_test_table}{chi_square_table}</div>"

    html_content += db_percentage_table
    html_content += test_results_table
    html_content += corr_matrix_table
    html_content += "<div style='page-break-before: always;'></div>"
    html_content += "<h2 style='text-align:center'>Reflection Usage Comparison </h2>"

    html_content += create_html_content(desc_ref_data)
    t_test_table_ref = create_html_table(reflections['test_results'], "T-Test Results")
    html_content += t_test_table_ref
    html_content += "<div style='page-break-before: always;'></div>"
    html_content += "<h2>Reflection (IoT vs Non-IoT)</h2>"
    html_content += "<div style='display:flex;'>"
    image_filename = os.path.basename(reflections['reflection_boxplots'])
    image_path = os.path.join(current_directory, image_filename)
    html_content += f"<img src='{image_path}' style='width:100%; padding:5px;'>"
    html_content += "</div>"

    # Apply Calibri font to the entire PDF
    css_style = "<style>body { font-family: Calibri, sans-serif; }</style>"
    html_content = css_style + html_content

    pdf_path = os.path.join(current_directory, '..', 'iotwhiz', 'public', 'out.pdf')
    try:
        options = {"enable-local-file-access": ""}
        pdfkit.from_string(html_content, pdf_path, configuration=config, options=options)
        return pdf_path
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None