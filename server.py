import socket
import threading

HOST,PORT = "127.0.0.1",3000
host_name = input("enter a hostname (default|127.0.0.1): ").strip()
port_name = input("enter a port number (default|3000): ").strip()

if len(host_name) > 2:
    HOST = host_name
if len(port_name) > 2:
    PORT = int(port_name)    

print(HOST,PORT)
HEADER_SIZE = 10

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((HOST,PORT))

server.listen(5)


print("Server is up. HOST: "+HOST+" PORT: "+str(PORT))


CONNECTED_CLIENTS = {}
class Connected_Client(socket.socket):
    def __init__(self,client,address):
        self.client = client
        self.address = address
        self.id = len(CONNECTED_CLIENTS)
        self.thread = threading.Thread(target=self.await_message)

    def await_message(self):
        full_msg = ""
        new_msg = True
        while True:
            msg = self.client.recv(16)
            if new_msg:
                msglen = int(msg[:HEADER_SIZE])
                new_msg = False
            full_msg += msg.decode("utf-8")
            if len(full_msg)-HEADER_SIZE == msglen:
                
                if full_msg[HEADER_SIZE:] == "CLIENT_DISCONNECT":
                    self.disconnect_socket()
                    break

                print(str(self.address)+": "+full_msg[HEADER_SIZE:])
                full_msg = ""
                new_msg = True

    def disconnect_socket(self):
        msg = "SERVER_DISCONNECT"
        full_msg = f"{len(msg):<{HEADER_SIZE}}"+msg
        self.client.send(bytes(full_msg,"utf-8"))
        disconnect_client(self.id)

def disconnect_client(id):
    print("Client Disconnected: "+str(CONNECTED_CLIENTS[id].address))
    CONNECTED_CLIENTS[id].client.close()
    del CONNECTED_CLIENTS[id]      

def await_connection():
    while True:

        # welcome message

        (client,address) = server.accept()

        print("New Client Connection: "+str(address))

        msg = f"Connection Successful: Welcome (HOST) {HOST} (PORT) {PORT} \n"
        full_msg = f"{len(msg):<{HEADER_SIZE}}"+msg

        client.send(bytes(full_msg,"utf-8"))

        # adding client to list of connected clients

        new_client = Connected_Client(client,address)
        CONNECTED_CLIENTS[new_client.id] = new_client
        new_client.thread.start()






clientconn_thread = threading.Thread(target=await_connection)
clientconn_thread.start()
