import socket
import time


# יצירת חיבור לשרת
def create_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 8080))
    print("Client connected to server.")
    return client_socket


# שליחת קובץ לשרת
def upload_file(client_socket, file_path):
    try:
        with open(file_path, "rb") as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                print(f"Sending {len(data)} bytes...")
                client_socket.send(data)
        # שליחת סימן סיום
        time.sleep(0.1)
        client_socket.send(b"DONE")
        print("Finish sending file.")
    except:
        print("File not found!")


# קבלת קובץ מהשרת
def get_file(client_socket, save_path):
    response = client_socket.recv(1024)
    if response == b"OK":
        with open(save_path, "wb") as file:
            while True:
                data = client_socket.recv(1024)
                if data == b"DONE":
                    print("Finish receiving file.")
                    break
                if not data:
                    break
                print(f"Received {len(data)} bytes...")
                file.write(data)
    else:
        print("File not found on server.")


# תפריט פשוט
print("1. Upload file")
print("2. Download file")
choice = input("Choose: ")

client_socket = create_client()

if choice == "1":
    filename = input("Enter filename to upload: ")
    client_socket.send(f"UPLOAD {filename}".encode())
    upload_file(client_socket, filename)

elif choice == "2":
    filename = input("Enter filename to download: ")
    client_socket.send(f"DOWNLOAD {filename}".encode())
    get_file(client_socket, f"downloaded_{filename}")

# חכה קצת לפני סגירה
time.sleep(0.5)
client_socket.close()