#!/bin/bash

# Zmienna dla wersji Pythona do zainstalowania
PYTHON_VERSION="3.11.4"

# Aktualizacja systemu
apt-get update && apt-get upgrade -y

# Instalacja wymaganych pakietów
apt-get install -y wget build-essential zlib1g-dev libffi-dev libssl-dev \
    libbz2-dev libreadline-dev libsqlite3-dev git

# Pobieranie i instalacja Pythona ze źródeł
cd /usr/src
wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz
tar xzf Python-$PYTHON_VERSION.tgz
cd Python-$PYTHON_VERSION
./configure --enable-optimizations
make altinstall

# Utworzenie wirtualnego środowiska z nowym Pythonem
/usr/local/bin/python3.11 -m venv /opt/myenv
source /opt/myenv/bin/activate

# Instalacja Ansible w wirtualnym środowisku
pip install --upgrade pip
pip install ansible ansible-core

# Pobranie repozytorium z plikami Ansible
git clone https://github.com/8tm/ansible-client.git /opt/ansible-client

# Konfiguracja SSH dla użytkownika ubuntu
mkdir -p /home/ubuntu/.ssh
chmod 700 /home/ubuntu/.ssh
curl https://github.com/8tm.keys > /home/ubuntu/.ssh/authorized_keys
chown ubuntu:ubuntu /home/ubuntu/.ssh/authorized_keys
chmod 600 /home/ubuntu/.ssh/authorized_keys

# Skonfiguruj skrypt, który uruchomi Ansible-playbook po restarcie
echo '@reboot root cd /opt/ansible-client && /opt/myenv/bin/ansible-playbook playbook.yml' > /etc/cron.d/run-ansible

# Restart systemu po zakończeniu
reboot
