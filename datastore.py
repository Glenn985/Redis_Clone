import time 
#the commands that will add and put etc
# we are implementing,key-value,retrieving value, deleting key,checking if key exists
#since redis is basically a key - value it will be designed as a dictionary at first, 
#

#for initial veriosn we will onluy implement, get , set , delete, nd exists
#here self.data will contain the TTL expiry also 

class DataStore:
    def __init__(self): #fyi self means instance of the class 
        self.data = {} 
        
    def Set(self , key , value, expiry_time=None):  # adding self before the parameters means that , its an instance of the class
        print("sending with set")
        self.data[key] = {"value": value, "expiry": expiry_time}
        return "OK"


    def get(self , key):
        value = self.data.get(key)
        if value is None:
            return None 
        expiry_time = value.get("expiry") 
        print(time.time(), "this is the time now")
        print("EXPIRY time", expiry_time)

        
        if expiry_time is not None and time.time() > expiry_time:
            print("Key has expired, removing it")
            self.data.pop(key, None) 
            return "NO VALUE"
        
        return value.get("value")

    def delete(self , key):
        self.data.pop(key)
        return "OK"

    
    def exists(self, key):
        if self.data.get(key) is not None:
            return True 
        return False  


    def set_expiry(self, key, expiry):
        if key not in self.data:
            return "ERROR: Key does not exist"
        self.data[key]["expiry"] = expiry
        return "OK"

    def set_with_ttl(self, key, value, ExpiryTime):
        print("Doing with set_with_ttl for key:", key)
        import time
        expiry = ExpiryTime
        self.data[key] = {"value": value, "expiry": expiry}
        return "OK"


