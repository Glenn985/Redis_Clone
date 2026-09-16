import socket
import time
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
     data = RespParser_encoder(data).encoder()
     data = data.encode("utf-8") # we do this because the data given is not encoded
     chunk_size = (len(data) + 7) // 8
     for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        print(f"Sending chunk: {chunk}")
        self.client.send(chunk)
        time.sleep(5)
            
        print("Printing encoded data" , data)
        print("size of data is", len(data)) 
        print("accepted by sent is ", data)
        #here sent is giving the bytes
        full_response = b""
    
     while b"\n" not in full_response:
            print("Receiving data chunk...")
            chunk =  self.client.recv(4096)
            print("Received data chunk:", chunk)
            response = chunk.decode("utf-8")
            if not chunk:
                print("No more data received from server")
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
   
    response = Conn.sender(command)
    print("Response:", response)





#*3\r\n$3\r\nSET\r\n$5\r\nglenn\r\n$4\r\n1231\r\n'
#FOR THIS WE NEED TO GET THE post number of the * and for the len we get of that part[3] we shdl oinly execute after we get hte n 