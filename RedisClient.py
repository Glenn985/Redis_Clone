import socket
from Resp_Encoder import RespParser_encoder
from RespParser_decoder import RespParser_decoder
class RedisClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client  = None

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        buffer_size = self.client.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        print(f"Buffer size: {buffer_size}") 
        self.client.connect((self.host, self.port))  # here the self.clietn will hvae the conn object 
        #thats why when i do send here I AM AGAIN encoding doubel encoding


    def sender(self, data):
        data = data.encode("utf-8") # we do this because the data given is not encoded
        self.client.send(data)
        print("Printing encoded data" , data)
        print("size of data is", len(data)) 
        print("accepted by sent is ", data)
        #here sent is giving the bytes
        full_response = b""
    
        while b"\n" not in full_response:
            print("Receiving data chunk...")
            chunk =  self.client.recv(4096)
            response = chunk.decode("utf-8")
            if not chunk:
                break
            full_response += chunk
        return full_response.decode("utf-8") # will give nothign if resposne is empty


Conn  = RedisClient("127.0.0.1", 45123)
Conn.connect() #conn is the socket object taht will connect to the server

while True:
    command = input("Enter command: ")

    if command.upper() == "QUIT":
        Conn.client.close()
        break 
    command = RespParser_encoder(command).encoder() 
    response = Conn.sender(command)
    print("Response:", response)

