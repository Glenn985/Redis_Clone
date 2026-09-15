#this is bascially simulating the terminal also when u do writer
import psutil
import asyncio
import time
import asyncio.queues
import time 
import Resp_Encoder as R #fyi we dont get encoded values so must use .encode()
import os


HOST = "127.0.0.1"
PORT = 45123


N = 10000
#N = 1000
queue = asyncio.Queue()

writers = []

async def one_client(i):
    try:
        reader, writer = await asyncio.open_connection(HOST, PORT)
        writers.append(writer)   
        writer.write(R.RespParser_encoder(f"SET key{i} value{i}\n").encoder().encode())  #just like writing in the command line itslef for that conn if it was on the terminal 
        #await writer.drain() ## wait till data is sent but nornaly this is very fast not needed 
        response = await reader.readline() 
        writer.write(R.RespParser_encoder(f"GET key{i}\n").encoder().encode()) 
        await writer.drain()
        # DON'T CLOSE HERE
        # writer.close()
        # await writer.wait_closed()
        

        return True
    except Exception as e:
        print("FAILED:", i, e)
        return False 
    


#this await lets us pause the task when there is a delay and let other tasks run on teh netwrok
#opening a network takes time, THE COMMAND TO OPEN DOES NOT , when that time is there we execute next command
# this is a heavy behaviour 
async def one_client_behavior_A(i): 
 try:
    reader , writer = await asyncio.open_connection(HOST,PORT)  #writer is the SOCKET object FYI a high level wrapper around 
    writers.append(writer)   
    # we want to simulate GET first 
    writer.write(R.RespParser_encoder(f"SET key{i} value{i}\n").encoder().encode()) 
    await writer.drain() # wait till the data is actualy sent


    response = await reader.readline()  
    writer.write(R.RespParser_encoder(f"GET key{i}\n").encoder().encode()) 
    await writer.drain()
    response = await reader.readline()
    writer.write(R.RespParser_encoder(f"SET key{i} value{i}\n").encoder().encode()) 
    await writer.drain()
    response = await reader.readline()

    # we are simulating a very heavy client - repeated requests , possible rate limiter here
    if response.decode().strip() != "OK": 
        for i in range(100):
            writer.write(R.RespParser_encoder(f"SET key{i} value{i}\n").encoder().encode()) 
            await writer.drain()
            response = await reader.readline()  


    return True 

 except Exception as e:
    print("FAILED:", i, e)
    return False

       
async def main():
    start = time.perf_counter()
    start_cpu = time.process_time()  
    tasks = []

    for i in range(N): 
     if (i % 10 == 0): 
        task = asyncio.create_task(one_client_behavior_A(i))
        tasks.append(task)
        continue
     task = asyncio.create_task(one_client(i))
     tasks.append(task)

    results = await asyncio.gather(*tasks) # this gatehrs and runs all the tasks together at hte same teim 
    end = time.perf_counter()
    end_cpu = time.process_time()
    print(results)
    print("CPU time:", end_cpu - start_cpu)
    print("Wall time:", end - start)
    successful = sum(results) # this will count total number of Treus and false
    failed = N - successful
    print("Successful:", successful)
    print("Failed:", failed)
    print("Time:", end - start)

    # KEEP ALL SUCCESSFUL CONNECTIONS ALIVE HERE
    print("Connections being held open:", len(writers))
    PID = os.getpid()
    print(PID)
    ram_megabytes = psutil.Process(PID).memory_info().rss / (1024 * 1024)
    print(f"Process [{PID}] RAM Usage: {ram_megabytes:.2f} MB")
    
    await asyncio.sleep(60) 
    # NOW close them after 60 seconds
    for writer in writers:
        writer.close()

    await asyncio.gather(
        *(writer.wait_closed() for writer in writers),
        return_exceptions=True
    )
   


asyncio.run(main())