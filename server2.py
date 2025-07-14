# === server_improved.py ===
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 8080))
server_socket.listen(5)
print("Listening for new connections...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    while True:
        command = client_socket.recv(1024).decode()
        print(f"Received command: {command}")

        if command == "UPLOAD":
            # קבלת קובץ מהלקוח
            with open("D:\ilay\courses\pythonProject16\me1.jpg", "wb") as file:
                while True:
                    data = client_socket.recv(1024)
                    if data == b"END":
                        print("File upload completed.")
                        break
                    file.write(data)

        elif command == "DOWNLOAD":
            # שליחת קובץ ללקוח
            with open("D:\ilay\courses\pythonProject16\me1.jpg", "rb") as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        client_socket.send("END".encode())
                        print("File sent to client.")
                        break
                    client_socket.send(data)

        elif command == "EXIT":
            print("Client disconnected.")
            client_socket.close()
            break

    # אופציונלי: לעצור את השרת אחרי שהלקוח מתנתק
    # break

server_socket.close()