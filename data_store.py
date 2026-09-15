#this is going to be the set and Get and all that t
# we are implementing,key-value,retrieving value, deleting key,checking if key exists
#since redis is basically a key - value it will be designed as a dictionary at first, 
#

#for initial veriosn we will onluy implement, get , set , delete, nd exists



class data_store:
    def init_self(self): #fyi self means instance of the class 
        self.data = {} 

    def Set(self , key , value):  # adding self before the parameters means that , its an instance of the class
        self.data[key] = value  

    def get(self , key):
        return self.data[key]

    def delete(self , key):
        self.data.pop(key)

    def exists(self key)


