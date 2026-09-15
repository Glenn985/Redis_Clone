string = "OK\r\n"
print(string.strip().split())

print(string[0])
print(string[0])
payload = string[1:].rstrip("\r\n")
print(payload)
