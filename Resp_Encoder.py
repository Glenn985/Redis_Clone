class RespParser_encoder:
    def __init__(self, message):
        self.stream = message 

    def encoder(self):
        Parts = self.stream.split()
        length = len(Parts) 
        
        # 1. Start with the array length followed by \r\n
        encoded = f"*{length}\r\n" 
        
        for part in Parts: 
            #r\n is always added ,
            encoded += f"${len(part)}\r\n{part}\r\n"
            
        return encoded



# message = input("Enter command: ")
# encoder = RespParser_encoder(message)
# result = encoder.encoder()
# print(repr(result))