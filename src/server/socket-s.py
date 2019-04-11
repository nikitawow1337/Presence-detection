# server.py

import socket                   # Import socket module

port = 1337                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
# host = socket.gethostname()     # Get local machine name
# host = socket.gethostbyname(socket.gethostname())
host = 'localhost'
print("Ip = ", host)
# host = 'localhost'
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print('Server listening....')

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)

    # client
    data = conn.recv(1024)
    # print('Server received', repr(data))

    # pa77ches
    client = str(data).split("|")
    print("Client ", client[0], "len ", len(client))
    data = data[len(client[0]) - 1:]
    # print("Data: ", data)
    # print("Data = ", client.count())
    client = client[0][2:].replace(":", "_")

    # write in file
    with open("clients.txt", 'a') as f:
        f.write(client)
        f.write("\n")

    # filename
    with open("faces/" + client + ".png", 'wb') as f:
        # print('file opened')
        f.write(data)
        while True:
            # print('receiving data...')
            data = conn.recv(1024)
            if not data:
                break
           # write data to a file
            f.write(data)
        print('Wrote file from: ', client)
        f.close()
    # s.close()
    # continue




    # nclients
    # data = conn.recv(1024)
    # nclients = data.decode("utf-8")

    #with open('clients.txt', 'w') as f:
    #    f.write(client)


    #filename = 'mypic.png'
    #f = open(filename,'rb')
    #l = f.read(1024)
    #while (l):
    #   conn.send(l)
    #   print('Sent ',repr(l))
    #   l = f.read(1024)
    #f.close()


    # print('Done sending')
    # conn.send('Thank you for connecting')
    # conn.close()
conn.close()
