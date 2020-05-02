---
layout: post
title:  "Inter-process communication with named pipes"
date:   2020-05-04 12:00:09 +0200
categories: posts
---
One of the simplest ways to implement inter-process communication is a named pipe, aka `fifo`. Because of the universal i/o model, the use of this approach is very similar to the sharing data with a regular file, but in the case of `fifo`, there is no writing to the filesystem.

The details of the `fifo` behavior, especially regarding blocking/non-blocking mode, might differ from OS to OS. 

Here is an example that demonstrates the use of the named pipes to send data from one process and receive it via another one. 

## Readers

Please use any of these readers. I provide two simple implementation one is in python3 another in golang.

**python:** [reader.py](https://github.com/andriikushch/andriikushch.github.io/blob/master/assets/code/4/reader.py)

```python
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

```

**go:** [reader.go](https://github.com/andriikushch/andriikushch.github.io/blob/master/assets/code/4/reader.go)

```go
package main

import (
    "bufio"
    "log"
    "os"
    "syscall"
)

func main() {
    path := "./fifo"

    _, err := os.Stat(path)

    if os.IsNotExist(err) {
        // try to create a named pipe
        if err := syscall.Mkfifo(path, 0600); err != nil {
            log.Panicln(err)
        }
    }

    f, err := os.Open(path)
    if err != nil {
        log.Panicln(err)
    }

    defer func() {
        if err := f.Close(); err != nil {
            log.Println(err)
        }
    }()

    for {
        b, err := bufio.NewReader(f).ReadByte()
        if err != nil{
            log.Panicln(err)
        }

        log.Printf("read : %d\n", b)
    }
}

```

## Writter

The following code expects pipe is already created.

**go:** [writter.go](https://github.com/andriikushch/andriikushch.github.io/blob/master/assets/code/4/writter.go)

```go
package main

import (
    "bytes"
    "encoding/binary"
    "log"
    "os"
    "time"
)

func main() {
    path := "./fifo"

    f, err := os.OpenFile(path, os.O_WRONLY, 0)
    if err != nil {
        log.Panicln(err)
    }

    defer func() {
        if err := f.Close(); err != nil {
            log.Println(err)
        }
    }()

    for i := uint8(0);;i++ {
        b := new(bytes.Buffer)
        err := binary.Write(b, binary.LittleEndian, i)
        if err != nil {
            log.Panicln(err)
        }
        if _, err := f.Write(b.Bytes()); err != nil {
            log.Panicln(err)
        }
        log.Printf("%d written to the fifo\n", i)
        time.Sleep(1*time.Second)
    }

    return
}

```

# Test

To run these examples, open two terminals and run one of the readers `python3 reader.py` or `go run reader.go` in one. And in another run  `go run writter.go`.

![demo.gif](/assets/images/4/demo.gif)


Please notice there will be a file with name `fifo` created in your directory. It should have a zero bytes size and be a type of pipe.

```bash
sh-3.2$ ls -lah fifo
prw-------  1 root  root     0B May  2 18:12 fifo
sh-3.2$ file fifo
fifo: fifo (named pipe)
```

If you see similar results, you have successfully used the named pipes for inter-process communication.

                                                                               