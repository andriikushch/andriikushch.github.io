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