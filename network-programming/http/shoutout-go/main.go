// simple program to shoutout the message sent to a server using the socket interface
package main

import (
	"fmt"
	"strings"
	"syscall"
)

func main() {
	fileDescriptor, err := syscall.Socket(syscall.AF_INET, syscall.SOCK_DGRAM, 0)
	if err != nil {
		panic(err)
	}

	err = syscall.Bind(fileDescriptor, &syscall.SockaddrInet4{Port: 8090, Addr: [4]byte{0, 0, 0, 0}})

	// You should change the buffer maximum bytes :)
	buf := make([]byte, 4)
	for {
		n, from, err := syscall.Recvfrom(fileDescriptor, buf, 0)
		if err != nil {
			panic(err)
		}

		outMsg := PrepareRecvMsg(buf, n)
		outMsgBytes := []byte(outMsg)
		fmt.Println(fileDescriptor)

		err = syscall.Sendmsg(fileDescriptor, outMsgBytes, []byte{}, from, 0)
		if err != nil {
			panic(err)
		}
	}
}

func PrepareRecvMsg(buf []byte, n int) string {
	// n represents the number of bytes that were actually read into the buffer.

	// when I call `syscall.Recvfrom(fileDescriptl, buf, 0)`, it attemps to read data from the socket into the buf byte slice. The `n` is the count of how many bytes were succesfully read.

	// This is usefull because the size of `buf`is often larger than the actual data received. By knowing `n` I can accurately slice `buf` to get the exact data received.
	msgBytes := buf[:n]
	outMsg := strings.ToUpper(string(msgBytes))
	return outMsg
}
