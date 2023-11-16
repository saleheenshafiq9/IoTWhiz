import subprocess

def decompile_apk(apk_path, output_dir):
    jadx_batch_path = "E://IIT//Last of BSSE//SPL-3//jadx//bin//jadx.bat"  # Replace with the path to your JADX JAR file and version
    command = [jadx_batch_path, "-d", output_dir, apk_path]

    try:
        subprocess.run(command, shell=True, check=True)
        print("Decompilation successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during decompilation: {e}")

if __name__ == "__main__":
    # Replace with the path to your APK and the desired output directory
    apk_path = "fillup.apk"
    output_directory = "path/to/output/directory"

    decompile_apk(apk_path, output_directory)
