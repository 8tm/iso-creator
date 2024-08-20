import os
import subprocess
import shutil
import requests

# Ścieżki wewnątrz kontenera
ISO_DIR = "/iso-builder/iso"
REPO_DIR = "/iso-builder/iso-creator"
ANSIBLE_DIR = "/iso-builder/ansible-client"
EXTRACT_DIR = "/iso-builder/custom_iso"
MOUNT_DIR = "/mnt/iso"
OUTPUT_DIR = "/output"

# URL do obrazu Ubuntu ISO
ISO_URL = "https://releases.ubuntu.com/24.04/ubuntu-24.04-live-server-amd64.iso"
ISO_NAME = "ubuntu-24.04-live-server-amd64.iso"

def download_iso():
    # Pobieranie obrazu ISO
    os.makedirs(ISO_DIR, exist_ok=True)
    iso_path = os.path.join(ISO_DIR, ISO_NAME)
    if not os.path.exists(iso_path):
        print("Downloading ISO...")
        response = requests.get(ISO_URL, stream=True)
        with open(iso_path, 'wb') as iso_file):
            shutil.copyfileobj(response.raw, iso_file)
        print("ISO downloaded.")
    else:
        print("ISO already exists, skipping download.")

def mount_iso():
    # Montowanie ISO
    if not os.path.exists(MOUNT_DIR):
        os.makedirs(MOUNT_DIR)
    subprocess.run(["mount", "-o", "loop", os.path.join(ISO_DIR, ISO_NAME), MOUNT_DIR], check=True)

def copy_iso_contents():
    # Kopiowanie zawartości ISO do katalogu roboczego
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)
    shutil.copytree(MOUNT_DIR, EXTRACT_DIR)

def unmount_iso():
    # Odmontowanie ISO
    subprocess.run(["umount", MOUNT_DIR], check=True)
    os.rmdir(MOUNT_DIR)

def copy_config_files():
    # Kopiowanie plików konfiguracyjnych z repozytorium do katalogu roboczego
    shutil.copy(os.path.join(REPO_DIR, "config/user-data"), EXTRACT_DIR)
    shutil.copy(os.path.join(REPO_DIR, "config/meta-data"), EXTRACT_DIR)
    shutil.copy(os.path.join(REPO_DIR, "config/vendor-data"), EXTRACT_DIR)
    shutil.copy(os.path.join(REPO_DIR, "config/post-install.sh"), EXTRACT_DIR)

def build_iso():
    # Budowanie zmodyfikowanego obrazu ISO
    output_iso_path = os.path.join(OUTPUT_DIR, "custom-ubuntu.iso")
    subprocess.run([
        "mkisofs", "-D", "-r", "-V", "Custom Ubuntu", "-cache-inodes", "-J", "-l",
        "-b", "isolinux/isolinux.bin", "-c", "isolinux/boot.cat",
        "-no-emul-boot", "-boot-load-size", "4", "-boot-info-table",
        "-o", output_iso_path, EXTRACT_DIR
    ], check=True)
    print(f"Custom ISO created at {output_iso_path}")

def main():
    download_iso()
    mount_iso()
    copy_iso_contents()
    unmount_iso()
    copy_config_files()
    build_iso()

if __name__ == "__main__":
    main()
