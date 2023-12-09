import requests

# api_key = '36b0de1dba01073d4a53a50d2060e79a0efc33337e95b3d7b7a448f7f6665e4e'
# sha256 = '23622BAADC12C422D70DA7AA7B6F0FF7B16F75C19E5B81F8B2F57A9F0E77151C'

def download_apk(api_key, sha256):
    url = f"https://androzoo.uni.lu/api/download?apikey={api_key}&sha256={sha256}"

    response = requests.get(url)

    if response.status_code == 200:
        # Extract filename or identifier to use for saving the file
        content_disposition = response.headers.get('content-disposition')
        file_size = response.headers.get('content-length')
        if content_disposition:
            filename = content_disposition.split("filename=")[1]
            filename = filename.strip('"')  # Clean up the filename if needed
        else:
            # If content disposition header isn't available, use the sha256 value
            filename = f"{sha256}.apk"

        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"File '{filename}' downloaded successfully!")
        return filename, file_size
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
