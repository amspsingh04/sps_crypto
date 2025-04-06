import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432

def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            st = input("Enter message: ")
            s.sendall(st.encode())
            data = s.recv(1024).decode()
            print(f"Data received is {data}")
            if data == 'BYE!':
                break
    
def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr=s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data=conn.recv(1024)
                print("Data from client is: ", data.decode())
                if(data.decode().lower() == "bye") or not data:
                    conn.sendall(b"BYE!")
                    s.close()
                    break
                st = input("Enter message: ")
                conn.sendall(st.encode())

__all__ = ["client", "server"]
