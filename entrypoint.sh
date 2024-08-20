#!/bin/bash

# Ustawienia repozytoriów
ISO_CREATOR_REPO="https://github.com/8tm/iso-creator.git"
ANSIBLE_CLIENT_REPO="https://github.com/8tm/ansible-client.git"

# Ścieżki wewnątrz kontenera
ISO_CREATOR_DIR="/iso-builder/iso-creator"
ANSIBLE_CLIENT_DIR="/iso-builder/ansible-client"

# Pobieranie repozytorium iso-creator
if [ ! -d "$ISO_CREATOR_DIR" ]; then
    echo "Cloning iso-creator repository..."
    git clone "$ISO_CREATOR_REPO" "$ISO_CREATOR_DIR"
else
    echo "iso-creator repository already exists, pulling latest changes..."
    git -C "$ISO_CREATOR_DIR" pull
fi

# Pobieranie repozytorium ansible-files
if [ ! -d "$ANSIBLE_CLIENT_DIR" ]; then
    echo "Cloning ansible-client repository..."
    git clone "$ANSIBLE_CLIENT_REPO" "$ANSIBLE_CLIENT_DIR"
else
    echo "ansible-client repository already exists, pulling latest changes..."
    git -C "$ANSIBLE_CLIENT_DIR" pull
fi

# Przejście do katalogu iso-creator i uruchomienie skryptu Python
cd "$ISO_CREATOR_DIR"
python3 build_iso.py
