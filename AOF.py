class AOF:
    def __init__(self,file):
        self.file = file 

    def append(self,data):
        with open(self.file,"a") as f:
            f.write(data +  "\n")
            f.flush()
        f.close()

    def delete(self):
        with open(self.file,"w") as f:
            f.truncate(0)
        f.close()

    def recover(self, command_handler):
        try:
            with open(self.file, "r") as f:
                for line in f:
                    command = line.strip()
                    if command:
                        command_handler.execute_aof(command)

        except FileNotFoundError:
            print("No AOF file found, starting fresh")

