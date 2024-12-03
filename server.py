import socket
import ssl

# Erstelle einen TCP/IP-Server-Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8443))  # Wähle eine Portnummer
server_socket.listen(5)
print("Server läuft und wartet auf Verbindungen...")

# SSL/TLS-Konfiguration
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.options |= ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2  # Verwende nur OpenSSL 1.0.1-typische Protokolle

# Zertifikate und Schlüssel für die Simulation
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

while True:
    # Warte auf eine eingehende Verbindung
    client_socket, addr = server_socket.accept()
    print(f"Verbindung von {addr} angenommen")
    
    # Verpacke die Verbindung in SSL/TLS
    ssl_socket = context.wrap_socket(client_socket, server_side=True)
    
    # Sende eine einfache Antwort an den Client
    ssl_socket.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHeartbleed Server Test")
    
    # Schließe die Verbindung
    ssl_socket.close()
