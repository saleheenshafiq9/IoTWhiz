import requests

api_key = "36b0de1dba01073d4a53a50d2060e79a0efc33337e95b3d7b7a448f7f6665e4e"
sha256 = "000406BC8F1883AF3436536BE1887FFEFBBD56782A5245AA62DA2343C90969DD"

url = f"https://androzoo.uni.lu/api/download?apikey={api_key}&sha256={sha256}"

response = requests.get(url)

if response.status_code == 200:
    # Extract filename or identifier to use for saving the file
    content_disposition = response.headers.get('content-disposition')
    if content_disposition:
        filename = content_disposition.split("filename=")[1]
        filename = filename.strip('"')  # Clean up the filename if needed
    else:
        # If content disposition header isn't available, use the sha256 value
        filename = f"{sha256}.apk"

    with open(filename, "wb") as file:
        file.write(response.content)
    print(f"File '{filename}' downloaded successfully!")
else:
    print(f"Failed to download file. Status code: {response.status_code}")
