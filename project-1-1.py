# import socket module
from socket import *
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789  #Prepare a server socket on a particular port
try:
    serverSocket.bind(('', serverPort))  # Fill in code to set up the port
    serverSocket.listen(1)

    while True:
        # Establish the connection
        print('Ready to serve ...')
        connectionSocket, addr = serverSocket.accept()  # Fill in code to get a connection
        try:
            message = connectionSocket.recv(1024).decode()  # Fill in code to read GET request
            filename = message.split()[1]

            if "../" in filename or "/grades/" in filename:
                forbidden_response = "HTTP/1.1 403 Forbidden\r\n\r\n<html><body><h1>403 Forbidden</h1></body></html>"
                connectionSocket.send(forbidden_response.encode())
                connectionSocket.close()
                continue  #Fill in security code

            f = open(filename, 'rb')
            outputdata = f.read() #Fill in code to read data from the file
            f.close()

            header = "HTTP/1.1 200 OK\r\n\r\n"  # Send HTTP header line(s) into socket
            connectionSocket.send(header.encode())  #Fill in code to send header(s)

            for i in range(len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
                connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        except IOError:
            not_found_response = "HTTP/1.1 404 Not Found\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>"
            connectionSocket.send(not_found_response.encode())  # Send response message for file not found
            connectionSocket.close()  #Close client socket
            continue  

finally:
    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data
