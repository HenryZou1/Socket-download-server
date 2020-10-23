# peer.py
'''
A P2P client
It provides the following functions:
- Register the content file to the index server (R)
- Contact the index server to search for a content file (D) 
    - Contact the peer to download the file
    - Register the content file to the index server
- De-register a content file (T)
- List the local registered content files (L)
- List the on-line registered content files (O)
'''
import os
import socket  # Import socket module
from collections import namedtuple

import pickle

s = socket.socket(socket.SOCK_DGRAM)  # Create a socket object

host = socket.gethostname()  # Get local machine name
port = 60003  # Reserve a port for your service.
s.connect((host, port))

# client is connected to the server
# define the PDU
PDU = namedtuple('PDU', ['data_type', 'data'])


# Functions
def select_name():
    return input('Please enter preferred username:')


def download_file(filename, address):
    rec_port = socket.socket()  # this is a TCP connection
    rec_port.connect(address)
    d_pdu = PDU('D', {'file_name': filename})
    b_pdu = pickle.dumps(d_pdu)
    rec_port.send(b_pdu)
    rec_filename = 'received_{}'.format(filename)
    with open(rec_filename, 'wb') as f:  # receive open file with received_file
        while True:
            message = rec_port.recv(1024)  # get pdu reply
            pdu = pickle.loads(message)  # decode binary pdu
            typepdu = pdu.data_type  # get PDU data type

            data = pdu.data  # get PDU data
            if (typepdu == 'D' or typepdu == 'F'):
                f.write(data.encode())  # write data to file convert to binary
            elif (typepdu == 'E'):
                print('Error detected')  # Error detected
                break
            if (typepdu == 'F'):  # After final pdu
                rec_port.close();
                f.close();
                break;
    return


def download(socket):
    pdu = socket.recv(1024)  # receive the request
    fpdu = pickle.loads(pdu)
    data = fpdu.data
    filename = data.get('file_name')
    with open(filename, 'r') as reader:  # open file with file name
        line, nextline = reader.read(100), reader.read(100)  # read line with a buffer to check if it is the file name max pdu size is 60 because of pickle overhead
        while True:  # infinte loop
            if (nextline):  # if next line

                namepdu = PDU('D', line)  # create a data pdu
                binarypdu = pickle.dumps(namepdu)  # create binary pdu
                socket.send(binarypdu)  # send binary pdu
                line = nextline  # change next to this line
                nextline = reader.read(100)  # read next line
            else:  # if its the final

                namepdu = PDU('F', line)  # create a data pdu
                binarypdu = pickle.dumps(namepdu)  # create binary pdu
                socket.send(binarypdu)  # send binary pdu
                reader.close()  # close the file
                break



    return


def listen():
    while True:
        fileReq_Socket, fileReq_addr = ss.accept()  # accept connection
        newpid = os.fork()
        if newpid == 0:
            download(fileReq_Socket)
        else:
            print('Peer connection accepted')
        # check the file name (it should be 'D' type)
        # send the file using 'C' type
        # if file doest not exist send 'E' pdu
        # there is no incomin`  g connection request, so go to the menu and ask the user for command


# create a server to listen to the file requests
'''
Here we config the server capability of the peers. As a server we need to specify ip address and ports. Since all the 
peers are inside the local network (IP=127.0.0.1), we need to use unique port numbers for each peers so they can
bind socket successfully. This can be done by generating random numbers and using try/except command to bind a socket.
Withing multiple attempt we can be sure that peer would eventually bind a socket with random port number. Here I do not
use this approach. Instead I asked the user to enter a port number manually. During the test, for each of the peers,
you will need to enter different port numbers for different peers. 
The '' for IP address means our server is listening to all IPs,
you can change it to socket.hostname instead like before.'''
inputs = []
outputs = []
exp = []
ss = socket.socket()  # this is a TCP connection
serverPort = int(input('Please enter listening port number for the download server:'))
try:
    ss.bind(('', serverPort))
except Exception:
    pass

ss.listen(5)
inputs.append(ss)
filename = 'Henry'
username = 'Henry'
exp.append(ss)

# service loop

'''
readable, writable, exceptional = select.select(inputs, outputs, exp, 1)
for sock in readable:  # check the incoming connection requests
    if sock is ss:
        fileReq_Socket, fileReq_addr = ss.accept()  # accept connection
        pdu = ss.recv(1024)  # receive the request
        print(pdu)
        # check the file name (it should be 'D' type)
        # send the file using 'C' type
        # if file doest not exist send 'E' pdu
        # there is no incomin`  g connection request, so go to the menu and ask the user for command
'''
newpid = os.fork()
if newpid == 0:
    listen()
else:
    while True:
        command = str(input('Please choose from the list below:\n'
                            '[O] Get online list\n'
                            '[L] List local files\n'
                            '[D] Download file\n'
                            '[R] Register a file\n'
                            '[T] De-register a file\n'
                            '[Q] Quit the program\n'))
        if command == 'O':
            o_pdu = PDU('O', {'Content List'})
            b_pdu = pickle.dumps(o_pdu)
            s.send(b_pdu)
            o_pdu = s.recv(1024)
            pdu = pickle.loads(o_pdu)
            data = pdu.data
            for i in data:
                name, file = i
                print('User name: ' + name + 'File: ' + file)

        if command == 'L':
            # list local files
            local_file = os.listdir('.')
            
            for name in local_file:
                print(name)
        if command == 'D':
            user = input('Please enter username of the file you want to download from:')
            file_name = input('What is the file name')
            s_pdu = PDU('S', {'peer_name': user, 'file_name': file_name})
            b_pdu = pickle.dumps(s_pdu)
            s.send(b_pdu)
            o_pdu = s.recv(1024)
            pdu = pickle.loads(o_pdu)
            address = pdu.data
            if pdu.data_type == 'A':
                print("Data is starting to download")
                download_file(file_name, address)

            elif pdu.data_type == 'E':
                print("No such file on server found with that user name. Try again.")
                # extract data_type
            # send 'O' type pdu
            # receive the list
            # print the list
            # ask user for the target file
            # create 'S' type pdu
            # send 'S' pdu to the index server
            # receive 'S' pdu in response
            # extract address
            # establish new connection to the peer

        if command == 'R':
            # get the file name
            # create 'R' pdu using username, filename, IPaddress and portnumber
            # send 'R' pdu
            # receive response pdu
            # if 'A', done
            # else if 'E',
            username = select_name()
            filename = str(input('Please Enter File Name'))
            while True:
                if os.path.isfile(filename):
                    break
                filename = str(input('Please Enter Valid local File Name'))
            while True:
                print(username + "File Name " + filename)
                r_pdu = PDU('R', {'peer_name': username, 'file_name': filename, 'address': (host, serverPort)})
                b_pdu = pickle.dumps(r_pdu)
                s.send(b_pdu)
                binary_pdu = s.recv(1024)
                pdu = pickle.loads(binary_pdu)
                data = pdu.data
                if pdu.data_type == 'A':
                    print(data.get('msg'))
                    print('\n')
                    break
                elif pdu.data_type == 'E':
                    print('Please Select new username a file was register with the same username\n')
                    username = select_name()
                    # extract data_type
        if command == 'T':

            filename = str(input('Please Enter File Name'))
            t_pdu = PDU('T', {'peer_name': username, 'file_name': filename, 'address': (host, serverPort)})
            b_pdu = pickle.dumps(t_pdu)
            s.send(b_pdu)
            binary_pdu = s.recv(1024)
            pdu = pickle.loads(binary_pdu)
            data = pdu.data
            # get the file name from user
            if pdu.data_type == 'A':
                print("Removed")
                print('\n')
            elif pdu.data_type == 'E':
                print('No such file was registered on your username\n')
        if command == 'Q':
            # for all the registered files:
            r_pdu = PDU('Q', {'peer_name': username, 'file_name': filename, 'address': (host, serverPort)})
            b_pdu = pickle.dumps(r_pdu)
            s.send(b_pdu)
            binary_pdu = s.recv(1024)
            pdu = pickle.loads(binary_pdu)
            data = pdu.data
            exit(0)

# quit the program
