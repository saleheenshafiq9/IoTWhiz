import pandas as pd
from pymongo import MongoClient
from scipy.stats import chi2_contingency, ttest_ind, mannwhitneyu

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['iotWhiz_new']

# Initialize an empty DataFrame

def get_database_strategy_percentages():
    df = pd.DataFrame()

    pd.set_option('display.max_columns', None)
    # Collect data from database
    for document in db.database_storage_data.find():
        # Extract relevant information
        app_type = "IoT" if document["iot_enabled"] else "non-IoT"
        strategies_found = document["strategies_found"]

        # Count occurrences of each strategy
        strategies_dict = {}
        for strategy, occurrences in strategies_found.items():
            # Handle empty strategies
            if occurrences is None:
                occurrences = []
            strategies_dict[strategy] = len(occurrences)

        # Create a row for the DataFrame
        row = {"app_type": app_type}
        row.update(strategies_dict)

        # Append the row to the DataFrame using `concat` instead of deprecated `append`
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    # Calculate percentages
    df_grouped = df.groupby("app_type").mean()*100
    test_analysis = perform_statistical_tests(df)
    chi_test_analysis = perform_chi_square_tests(df)["chi_square_test_results"]
    corr_analysis = perform_chi_square_tests(df)["correlation_analysis"]

    return {
        "database_strategy_percentages": df_grouped.to_dict(), 
        "statistical_test_results": test_analysis,
        "chi_test_results" : chi_test_analysis,
        "corr_analysis": corr_analysis
    }


# Perform statistical analyses
def perform_statistical_tests(df):
    results = {}
    for col in df.columns[1:]:
        # Check if data is numerical or categorical
        if pd.api.types.is_numeric_dtype(df[col]):
            # Perform t-test if numerical
            stat, p = ttest_ind(df[col][df["app_type"] == "IoT"], df[col][df["app_type"] == "non-IoT"])
            test_name = "t-test"
        else:
            # Perform Mann-Whitney U test if categorical
            stat, p = mannwhitneyu(df[col][df["app_type"] == "IoT"], df[col][df["app_type"] == "non-IoT"])
            test_name = "Mann-Whitney U test"

        results[f"{test_name} for {col}"] = {"stat": stat, "p": p}

    return results

# Perform chi-square test for each strategy
def perform_chi_square_tests(df):
    results = {}
    for col in df.columns[1:]:
        # Check if data is present for both app types
        if df[col][df["app_type"] == "IoT"].any() and df[col][df["app_type"] == "non-IoT"].any():
            table = pd.crosstab(df["app_type"], df[col])
            chi2, p, dof, expected = chi2_contingency(table)
            results[f"Chi-square test for {col}"] = {"chi2": chi2, "p": p, "df": dof}
    return {"chi_square_test_results": results, "correlation_analysis": df.corr().to_dict()}
