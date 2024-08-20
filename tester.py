import socket

def check_server(host, port, attempts=10, timeout=2):
    successful_attempts = 0

    for i in range(attempts):
        try:
            with socket.create_connection((host, port), timeout) as sock:
                successful_attempts += 1
        except (socket.timeout, socket.error):
            pass

    success_rate = (successful_attempts / attempts) * 100

    if success_rate == 100:
        return f"Komunikacja z serwerem {host} na porcie {port} na 100%. Serwer odpowiada poprawnie."
    elif success_rate > 0:
        return f"Komunikacja z serwerem {host} na porcie {port} na {success_rate}%. Serwer gubi połączenia."
    else:
        return f"Brak komunikacji z serwerem {host} na porcie {port}. Serwer nie odpowiada."


host = "example.com"
port = 80
print(check_server(host, port))
