##an overweiw of using selector here, u do , in the socket itslef either 
#event_read, event_write this is a poll or a event that will notify the  key.fileobj 
#we can always keep event write , but this is bad becasue , it will constantly notify us even when we have nothing to write, wasting CPU cycles
# ACtual redis does not do like this, once the write is ready it will handle it immediately rather than constantly watching for write events

import socket
import selectors
from Commandhandler import CommandHandler
from datastore import DataStore
from RespParser_decoder import RespParser_decoder
from Resp_Encoder import RespParser_encoder


datastore = DataStore()
handler = CommandHandler(datastore) # handler execute does all the transfer , everything about hte data

class RedisServer:
    def __init__(self, host, port, handler,AOF):
        self.handler = handler
        self.host = host
        self.port = port
        self.selector = selectors.DefaultSelector()
        self.output_buffers = {}
        self.AOF = AOF #this is a boolean

    def setUp(self):
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM 
        )
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#preventing the address already in use
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        buffer_size = self.server.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)#just fyi getting buffer size info 
        print(f"Buffer size: {buffer_size}") 

        self.server.setblocking(False) 
        # this is what symbolyses that the server will not simply wait for the thing to finish
        # When server socket becomes READABLE,
        # call accept_connection()
        self.selector.register(
            self.server,
            selectors.EVENT_READ,
            self.accept_connection
        )
    def handle_request(self, request,AOF):
        return self.handler.execute(request,AOF) 
       
    def accept_connection(self, server_socket, mask):
        client, address = server_socket.accept()
        print("Connected:", address)
        # Don't let recv() block
        client.setblocking(False)
        # When THIS client has data ready,
        # call handle_client(), so each csocket is running the handle client
        self.selector.register( 
            client,
            selectors.EVENT_READ,
            self.handle_client
        )

    
    def handle_client(self, client, mask):
            ## THE SOCKET WILL BE READY FOR READING first IE SERVER WILL READ WHAT CLIENT HAS TO SAYYYY
            ##selectors.EVENT_READ will be triggered when there is data to read form the client ie clietn.send
            if mask & selectors.EVENT_READ: 
                print("Socket ready for reading")
                try:
                    data = client.recv(4096) 
                    if data == b"":
                                    print("Client disconnected")
                                    self.selector.unregister(client)
                                    self.output_buffers.pop(client, None)
                                    client.close()
                                    return 
                    
                except BlockingIOError:
                    return 
            ## this is for data disconection ti will sned b"" byte"
            #post getting the data ie after event_read,
            # we are allowing for massive amoubts of data to be sent
                request = data.decode("utf-8").strip()
                print("Received:", request) 
                print("AOF state:", self.AOF)
                response = self.handle_request(request,self.AOF)
                print("Response: FOR TEST ", response)
                if response == None:
                     response = "+NONE\r\n"
                response_bytes = RespParser_encoder(response).encoder().encode()
                print("Response length:", len(response_bytes))
                self.output_buffers.setdefault(client, b"")
                self.output_buffers[client] += response_bytes
            # We now have response bytes waiting to be sent.
            # Keep watching READ for more incoming data, and ALSO
            # start watching WRITE so we know when the socket can
            # accept response bytes.
                self.selector.modify( #does both the event write and hte event read at the same time 
                client,
                selectors.EVENT_READ | selectors.EVENT_WRITE, #watches out for both read or write 
                self.handle_client
                )
        ## checking if the clietn socket is ready for writing
            ## checking if the clietn socket is ready for writing 
            ## this is post the reading thign , we awant to check if socket is ready for writing
            if mask & selectors.EVENT_WRITE: 
             print("Socket ready for writing")
            #mask is the integer bitmap that will show which events are ready for this socket (read or write)
             pending_data = self.output_buffers[client]
             if pending_data:
                try:
                    sent = client.send(pending_data)
                    print(
                        "Sent",
                        sent,
                        "bytes to",
                        client.getpeername()
                    )
                    # remove the bytes that were successfully sent
                    self.output_buffers[client] = pending_data[sent:]
                except BlockingIOError:
                    print(
                        "Socket cannot currently accept more data:",
                        client.getpeername() #peername is the name of the socket 
                    )
                    return
            # if we have FINISHED sending everything
             if not self.output_buffers[client]:
                print(
                    "Finished sending to",
                    client.getpeername()
                )
                # go back to only watching READ 
                self.selector.modify(
                    client,
                    selectors.EVENT_READ,
                    self.handle_client
                ) 
    def run(self):
        while True:
            events = self.selector.select() 
            for key, mask in events:
                #key holds the sockets instance ,mask is what tells u what to do ie read or write
                sock = key.fileobj
                print(
                "SELECTOR RETURNED:",
                sock.fileno(), 
                sock.getpeername() if sock is not self.server else "SERVER SOCKET"
            )
                callback = key.data #this is where hte handle client is runH
                callback(
                    key.fileobj,
                    mask
                )
         
server = RedisServer(
    host="127.0.0.1",
    port=45123,
    handler=handler,
    AOF = True
)
server.setUp()
handler.recover_from_aof("appendonly.txt")
server.run()