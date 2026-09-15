from datastore import DataStore 
from Commandhandler import CommandHandler
from parser import Parser 


store = DataStore() #instace of datastore
handler = CommandHandler(store) #instance of command handler with the datastore instance
parser = Parser()


request = parser.parse("SET X SAI") 
print(request)
print(handler.execute(request)) 


request = parser.parse("GET X")
print(handler.execute(request))