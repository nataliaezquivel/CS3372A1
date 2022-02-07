#!/usr/bin/env python3

import socket
from sys import argv


def main(): 
    print('Processing arguments...')
    # argv array
    if (len(argv) < 2): 
        port = 8080
        print('Default port: %s' % port)
    # print the first argument supplied
    else:
        port = int(argv[1])
        print('Port entered: %s' % port)

    sock(port)
    return

def sock(port):
    # Define socket host and port
    SERVER_HOST = '127.0.0.1'#socket.gethostname() #'0.0.0.0'
    SERVER_PORT = port
    print('Server host: ', SERVER_HOST)
    print('Server port: ', SERVER_PORT)
    
    # Create socket

    # SERVER
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print('Listening on port: ', SERVER_PORT)
    
    # CLIENT
    while True:
        # Wait for client connections
        client_connection, client_address = server_socket.accept()
        # Get the client request
        request = client_connection.recv(1024).decode('utf-8')
        print(request)
        # Split request from spaces
        str_list = request.split(' ')
        # First string is a method
        method = str_list[0]
        # Second string is a request file
        req_file = str_list[1]
        print('Client request: ', req_file)
        # File reading
        sentFile = req_file.split('?')[0] 
        sentFile = sentFile.lstrip('/')
        if (sentFile == ''):
            # index file loaded as default
            sentFile = 'you-got-this-meme.jpg'
        try:
            file = open(sentFile, 'rb')
            response = file.read()
            file.close()
            # Send HTTP response
            header = 'HTTP1.1 200 OK\n'

            if (sentFile.endswith(".jpg")):
                filetype = 'image/jpg'
            elif (sentFile.endswith(".png")):
                filetype = 'image/png'
            elif (sentFile.endswith(".jpeg")):
                filetype = 'image/jpeg'
            header += 'Content Type: ' + str(filetype) + '\n\n'
        except:
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = '<html><body><center><h3>Error 404: File not found</h3>Python HTTP Server</p></center></body></html>'.encode('utf-8')
        # Send HTTP response
        final_response = header.encode('utf-8')
        final_response += response
        client_connection.send(final_response)
        client_connection.close()

    # Close socket
    server_socket.close()
    # sys.exit()

if __name__ == '__main__':
    main()
