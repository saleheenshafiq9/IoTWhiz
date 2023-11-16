import requests

api_key = "36b0de1dba01073d4a53a50d2060e79a0efc33337e95b3d7b7a448f7f6665e4e"
sha256 = "E64B9079286796DEDC0FC652BFB28B152AB21833A2B5C140A5DE570C7C4EB9A7"

url = f"https://androzoo.uni.lu/api/download?apikey={api_key}&sha256={sha256}"

response = requests.get(url)

if response.status_code == 200:
    with open("downloaded_file.apk", "wb") as file:
        file.write(response.content)
    print("File downloaded successfully!")
else:
    print(f"Failed to download file. Status code: {response.status_code}")
