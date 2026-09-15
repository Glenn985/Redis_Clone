import time
class RDB_SNAP:
    def __init__(self,datastore,file):
        self.datastore = datastore
        self.file = file

    def save(self): # we deny the entry of a key if it has expired 
        with open(self.file, "w") as f:
            for key, value in self.datastore.data.items():
                expiry = value["expiry"] 

                if expiry != None and expiry > time.time():
                    f.write(f"{key} {value['value']} {expiry}\n")  
                if expiry == None:
                    f.write(f"{key} {value['value']} None\n") 



    def Load(self):
        with open(self.file, "r") as f:
            for line in f:
                key, value, expiry = line.strip().split()
                if expiry == "None":
                    expiry = None
                else:
                    expiry = float(expiry)
                if expiry is not None and expiry < time.time():
                    continue
                self.datastore.data[key] = {"value": value, "expiry": expiry}

        