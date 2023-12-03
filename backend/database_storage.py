import os
import re

def search_database_related_strategies(project_folder):
    database_patterns = {
        'Cursor': r'Cursor\b',
        'ContentResolver': r'getContentResolver\(',
        'MediaStoreQueries': r'MediaStore\b',
        'SQLiteOpenHelper': r'SQLiteOpenHelper\b',
        'RoomDatabasePatterns': r'@(Entity|Dao|Database)\b|extends RoomDatabase\b',
        'RealmDatabase': r'Realm\b',
        'FirebaseDatabase': r'FirebaseDatabase\b',
        'ObjectBoxDatabase': r'ObjectBox\b',
        'SQLiteDatabase': r'SQLiteDatabase\b',
        # Add more patterns for other database storage strategies
    }

    strategies = {}

    for strategy_name, pattern in database_patterns.items():
        occurrences = []
        for root, _, files in os.walk(project_folder):
            for file_name in files:
                if file_name.endswith(".java"):
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, 'r') as file:
                            content = file.read()
                            matches = re.findall(pattern, content)
                            if matches:
                                occurrences.extend([(file_path, i + 1, line.strip()) 
                                                    for i, line in enumerate(content.split('\n')) 
                                                    if re.search(pattern, line)])
                    except Exception as e:
                        print(f"Error parsing file {file_path}: {e}")
        strategies[strategy_name] = occurrences

    return strategies

def describe_database_strategies(strategies):
    descriptions = {
        'Cursor': "Several occurrences of Cursor objects being used for querying databases (query, getCursor, etc.)",
        'ContentResolver': "Calls to getContentResolver() for interacting with data from various sources",
        'MediaStoreQueries': "Queries using MediaStore to access media-related data",
        'SQLiteOpenHelper': "The presence of SQLiteOpenHelper indicates the use of SQLite database management",
        'RoomDatabasePatterns': "Although explicit Room annotations are not found, usage of @Entity, @Dao, and Room's functionalities are common in database-related contexts",
        'RealmDatabase': "Usage of Realm database for data storage",
        'FirebaseDatabase': "Utilization of FirebaseDatabase for cloud-based data storage",
        'ObjectBoxDatabase': "Usage of ObjectBox for object-oriented database management",
        'SQLiteDatabase': "Usage of SQLiteDatabase for managing SQLite databases",
        # Add descriptions for other strategies
    }

    result = {}
    for strategy_name, occurrences in strategies.items():
        if occurrences:
            strategy_occurrences = []
            for file_path, line_number, line_content in occurrences:
                strategy_occurrences.append({
                    'File': file_path,
                    'Line': line_number,
                    'Content': line_content
                })
            result[strategy_name] = {
                'Description': descriptions[strategy_name],
                'Occurrences': strategy_occurrences
            }
    return result

# # Provide the relative path to your Android project folder
# project_relative_path = 'backend/goodtime'
# strategies_found = search_database_related_strategies(project_relative_path)
# strategies_description = describe_database_strategies(strategies_found)
