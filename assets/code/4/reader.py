import os

try:
    path = "./fifo"
    os.mkfifo(path, 0o600)  # try to create a named pipe
except FileExistsError:
    print("file already exists")

with open("./fifo", "r") as f:
    while 1:
        byte = f.read(1)
        print("read : {}".format(ord(byte)))
