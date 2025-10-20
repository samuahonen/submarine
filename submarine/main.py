import socket

HOST = '192.168.1.10'  
PORT = 5000         

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to server {HOST}:{PORT}")
    
    while True:
        # Send message to server
        msg = input("Your message: ")
        s.sendall(msg.encode())
        
        # Receive response from server
        data = s.recv(1024)
        print(f"Server says: {data.decode()}")
