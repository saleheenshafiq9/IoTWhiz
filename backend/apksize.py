import requests
import os, csv
from pymongo import MongoClient
from main import store_data_in_mongodb

url = "https://androzoo.uni.lu/api/download"
apikey = "36b0de1dba01073d4a53a50d2060e79a0efc33337e95b3d7b7a448f7f6665e4e"
sha256_list = [
    "000022029986C121B891C377DB8737A70AFDC6A26C9E4517BF029878FF605470"
]

def apk_size():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_directory, 'helper.csv')

    client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
    db = client['iotWhiz_new']  # Replace with your database name

    with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header row

            for row in csv_reader:
                print(row)
                sha256 = row[0]  # Assuming SHA256 is in the first column
                received_iot_enabled = int(row[2])  # Assuming status is in the second column as 0 or 1
                params = {
                    "apikey": apikey,
                    "sha256": sha256
                }

                response = requests.head(url, params=params)

                # Check if the request was successful
                if response.status_code == 200:
                    # Extract file size from the response headers
                    file_size = response.headers.get('content-length')
                    print(f"for {sha256}, the size is {file_size/(1024*1024)} MB")
                else:
                    print(f"Failed to get file size for SHA256: {sha256}")

                data_to_store = {
                    "folder_path": sha256,
                    "apk_size": file_size,
                    "iot_enabled": received_iot_enabled
                }

                store_data_in_mongodb("downloads", sha256, data_to_store)
