import socket
import time

# יצירת סוקט TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# קביעת כתובת IP ופורט
server_socket.bind(("127.0.0.1", 8080))

# המתנה לחיבורים (עד 5)
server_socket.listen(5)
print("Listening for new connections...")


# קבלת קובץ מהלקוח
def download_file(client_socket, file_path):
    with open(file_path, "wb") as file:
        while True:
            data = client_socket.recv(1024)
            if data == b"DONE":
                print("File finished.")
                break
            if not data:
                break
            print(f"Received {len(data)} bytes...")
            file.write(data)


# שליחת קובץ ללקוח
def send_file(client_socket, file_path):
    try:
        with open(file_path, "rb") as file:
            client_socket.send(b"OK")
            while True:
                data = file.read(1024)
                if not data:
                    break
                print("Sending 1024 bytes...")
                client_socket.send(data)
        # סימן סיום
        time.sleep(0.1)
        client_socket.send(b"DONE")
    except:
        client_socket.send(b"NOT_FOUND")


# לולאה ראשית
while True:
    # קבלת חיבור מלקוח
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    # קבלת פקודה
    command = client_socket.recv(1024).decode()

    if command.startswith("UPLOAD"):
        filename = command.split()[1]
        download_file(client_socket, filename)

    elif command.startswith("DOWNLOAD"):
        filename = command.split()[1]
        send_file(client_socket, filename)

    # חכה קצת לפני סגירה
    time.sleep(0.5)
    client_socket.close()