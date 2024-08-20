# Używamy obrazu bazowego Ubuntu
FROM ubuntu:24.04

# Instalacja niezbędnych narzędzi
RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    genisoimage \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalacja pakietów Python
RUN pip3 install --break-system-packages requests

# Skopiowanie skryptu entrypoint.sh do obrazu
COPY entrypoint.sh /entrypoint.sh

# Ustawienie katalogu roboczego
WORKDIR /iso-builder

# Ustawienie punktu wejścia
ENTRYPOINT ["/entrypoint.sh"]
