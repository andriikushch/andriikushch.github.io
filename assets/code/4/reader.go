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