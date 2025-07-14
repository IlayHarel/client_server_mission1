# === client_improved.py ===
import socket


def create_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 8080))
    print("Client connected to server.")
    return client_socket


def upload_file(client_socket, file_path):
    client_socket.send("UPLOAD".encode())

    with open(file_path, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                # שליחת סימן סיום
                client_socket.send("END".encode())
                print("Finish sending file.")
                break
            client_socket.send(data)


def download_file(client_socket, save_path):
    client_socket.send("DOWNLOAD".encode())

    with open(save_path, "wb") as file:
        while True:
            data = client_socket.recv(1024)
            if data == b"END":
                print("File download completed.")
                break
            file.write(data)


# תוכנית ראשית
client_socket = create_client()

while True:
    print("\n1. Upload file")
    print("2. Download file")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        file_path = input("Enter file path to upload: ")
        upload_file(client_socket, file_path)
    elif choice == "2":
        save_path = input("Enter path to save downloaded file: ")
        download_file(client_socket, save_path)
    elif choice == "3":
        client_socket.send("EXIT".encode())
        break

client_socket.close()