import os
import subprocess

def decompile_apk(apk_path, output_dir):
    apk_name = os.path.splitext(os.path.basename(apk_path))[0]  # Extract the APK file name without extension
    output_directory = os.path.join(output_dir, apk_name)  # Create a folder path using the APK's name

    jadx_batch_path = "E://IIT//Last of BSSE//SPL-3//jadx//bin//jadx.bat"  # Replace with the path to your JADX JAR file and version
    command = [jadx_batch_path, "-d", output_directory, apk_path]

    try:
        subprocess.run(command, shell=True, check=True)
        print("Decompilation successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during decompilation: {e}")

if __name__ == "__main__":
    # Replace with the path to your APK and the desired output directory
    apk_path = "itesmartplug.apk"
    output_directory = "backend"

    decompile_apk(apk_path, output_directory)
