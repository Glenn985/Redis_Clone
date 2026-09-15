#store is the datastore object
#pirmary function of hte commandhandler is to figure out which Datastore method to call 
# is used to implement whats in the datastore
from datastore import DataStore
import io 
from Resp_Encoder import RespParser_encoder
from RespParser_decoder import RespParser_decoder
from datetime import datetime

import AOF
aof = AOF.AOF("appendonly.txt")
import time 
#we are ignoring the GET command for AOF logging




class CommandHandler:
    def __init__(self, store: DataStore): #store is of hte class DATASTORE , we are using hte methods of datastore through the instance of the objcet class
          self.store = store 
          # this is the data dictioanary object
    #request is a message likely to be in the list 
    def execute(self, request,AOF):
       print(AOF ," this is the state of AOF")
       server_now = datetime.now()
       request = RespParser_decoder(request).parse()
       message = request 
       print("Parsed request:", message) # request is already parsed into a list by RespParser_decoder
       print("We are at commandhandler for recieve request")
       print(message[0]) 
       try :
        print("Length of message:", len(message))
        if message[0] == "SET" and len(message) >3: 
            if AOF:
             aof.append(f"SET {message[1]} {message[2]}")
            print("This is the parsed message" ,message)
            key = message[1]
            value = message[2] 
            if self.store.exists(key):
                return "ERROR: Key already exists" 

            if message[3] == "EXP":
                expire_time = int(message[4]) 
                expire_time = expire_time + time.time()
                if AOF:
                 aof.append(f"SET {message[1]} {message[2]} EXP {expire_time}")
                return self.store.set_with_ttl(key, value, expire_time)
            return self.store.Set(key,value,None)  

        if message[0] == "SET" and len(message) <=3:  
              key = message[1]
              if self.store.exists(key):
                  return "ERROR: Key already exists"
              print("in set with lwoer than 3")
              value = message[2] 
              if AOF == True:
               print("Appending DELETE command to AOF")
               aof.append(f"SET {key} {value}")
              return self.store.Set(key, value, None)

        if message[0] == "EXPIRY":
            key = message[1] 
            expiry = message[2]
            if not self.store.exists(key):
                return "ERROR: Key does not exist"
            return self.store.set_expiry(key, expiry)

        if message[0] == "BIGGET":
            key = message[1]
            return self.store.get(key) * 1000000

        elif message[0] == "GET": 
            key  = message[1]  
            current_time = int(server_now.timestamp())
            print("Currently in KEY", key)
            if self.store.data[key]["expiry"] is not None and self.store.data[key]["expiry"] <= current_time:
                self.store.delete(key)
                return None
            return self.store.get(key)  

        elif message[0] == "BIG":
            key = message[1]
            if not self.store.exists(key):
                return "ERROR: Key does not exist"
            return self.store.get(key) * 100000000

        elif message[0] == "DELETE": 
            key = message[1] 
            if not self.store.exists(key):
                return "ERROR: Key does not exist" 

            
            if AOF:
             
             aof.append(f"DELETE {key}" )
            return self.store.delete(key)
        
        elif message[0] == "EXISTS":
            key = message[1]
            return self.store.exists(key)
        
        else:
            return "ERROR + unkown command" 
        
       except Exception as e:
            return f"ERROR: {str(e)}"
        # nothing else to do here



    def recover_from_aof(self, file):
         with open(file, "r") as f:
            for line in f:
                message = line.strip().split()
                if not message:
                    continue
                if message[0] == "SET":
                    key = message[1]
                    value = message[2]
                    if len(message) > 3 and message[3] == "EXPIRY":
                        expiry_time = int(message[4])
                        ttl = expiry_time - int(time.time() )
                        self.store.set_with_ttl(key, value, ttl)
                    else:
                        self.store.Set(key, value, None)
                elif message[0] == "DELETE":
                    key = message[1]
                    if self.store.exists(key):
                        self.store.delete(key)
        
    
         

    