import requests
from tqdm import tqdm  # Import tqdm for progress bar

def download_apk(api_key, sha256):
    url = f"https://androzoo.uni.lu/api/download?apikey={api_key}&sha256={sha256}"

    response = requests.get(url, stream=True)  # Use stream=True to enable streaming

    if response.status_code == 200:
        # Extract filename or identifier to use for saving the file
        content_disposition = response.headers.get('content-disposition')
        file_size = int(response.headers.get('content-length'))  # Get the file size
        if content_disposition:
            filename = content_disposition.split("filename=")[1]
            filename = filename.strip('"')  # Clean up the filename if needed
        else:
            # If content disposition header isn't available, use the sha256 value
            filename = f"{sha256}.apk"

        # Use tqdm to create a progress bar for the download
        with open(filename, "wb") as file, tqdm(
            total=file_size,
            unit='B',
            unit_scale=True,
            desc=filename,
            ascii=True,
            ncols=100
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                progress_bar.update(len(data))  # Update the progress bar

        print(f"File '{filename}' downloaded successfully!")
        return filename, file_size
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
