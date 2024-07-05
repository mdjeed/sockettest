import socket



HOST = '192.168.125.165'  
PORT = 65432

def receive_file(s, file_path):
    with open(file_path, 'wb') as f:
        while True:
            data = s.recv(4096)
            if b'FILE_TRANSFER_COMPLETE' in data:
                data = data.replace(b'FILE_TRANSFER_COMPLETE', b'')
                f.write(data)
                break
            f.write(data)
    print(f"File {file_path} downloaded successfully.")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        confirmation = s.recv(1024).decode()
        if confirmation == 'Connection successful':
            print("Connected to the server successfully.")
            while True:
                command = input("Enter command to execute (type 'exit' to close, 'download <filepath>' to download a file): ")
                s.sendall(command.encode())
                if command.lower() == 'exit':
                    print("Closing connection...")
                    break
                elif command.startswith('download '):
                    file_path = command.split(' ', 1)[1]
                    receive_file(s, file_path)
                else:
                    data = s.recv(4096)
                    print('Received:', data.decode())
        else:
            print("Failed to connect to the server.")
except ConnectionRefusedError:
    print("Connection failed: The server refused the connection.")
except socket.timeout:
    print("Connection failed: The connection timed out.")
except Exception as e:
    print(f"Connection failed: An unexpected error occurred: {e}")