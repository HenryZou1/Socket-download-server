# index_server.py
'''
Index Server 
Message types:
R - used for registration
A - used by the server to acknowledge the success
Q - used by chat users for de-registration
D - download content between peers (not used here)
C - Content (not used here)
S - Search content
E - Error messages from the Server
'''

import socket  # Import socket module
from collections import namedtuple
import pickle
import os
from multiprocessing import Process, Manager

port = 60000 # Reserve a port for your service.
s = socket.socket(socket.SOCK_DGRAM)  # Create a socket object
host = socket.gethostname()  # Get local machine name
s.bind((host, port))  # Bind to the port
s.listen(5)  # Now wait for client connection.
# server is up and listening
print('Server listening....')

PDU = namedtuple('PDU', ['data_type', 'data'])
Files_List = namedtuple('Files_List', ['peer_name', 'file_name', 'address'])
fList = []  # list of files, containing Files_List namedtuples


def service():

    while True:
        binary_pdu = conn.recv(1024)
        print("Server List:")
        print(fList)
        # receiving the binary_pdu = conn.recv(100)
        # convert pdu from binary to pdu object using pickle
        pdu = pickle.loads(binary_pdu)
        # extract the type from pdu, type = pdu.data_type
        # check data_type0
        data_type = pdu.data_type
        data = pdu.data
        print("Recieved data type: "+data_type)

        # if 'R'
        # check list of files
        # if file does not already exist (new)
        # create new Files_List object
        # send 'A' type pdu
        # send 'E' type pdu
        if data_type == 'R':
            p_peer_name = data.get('peer_name')
            p_file_name = data.get('file_name')
            p_peer_address = data.get('address')
            already_exists = False
            for i in fList:
                if i.peer_name == p_peer_name and i.file_name == p_file_name:
                    e_pdu = PDU('E', {'msg': 'File already exists'})
                    b_pdu = pickle.dumps(e_pdu)
                    conn.send(b_pdu)
                    already_exists = True
                    break
            if not already_exists:
                file = Files_List(p_peer_name, p_file_name, p_peer_address)
                fList.append(file)
                a_pdu = PDU('A', {'msg': 'Successfully Registered'})
                b_pdu = pickle.dumps(a_pdu)
                conn.send(b_pdu)
        # else if 'S'
        # check the fList
        # if the file exists, send the file
        # else send 'E' pdu
        elif data_type == 'S':
            p_peer_name = data.get('peer_name')
            p_file_name = data.get('file_name')
            found_content = False
            for d in fList:
                if d.peer_name == p_peer_name and d.file_name == p_file_name:
                    target = d
                    found_content = True
                    break
            if found_content:
                pdu = PDU('A', target.address)
                b_pdu = pickle.dumps(pdu)
                conn.send(b_pdu)
            else:
                e_pdu = PDU('E', {'msg': 'Record does not exists on the list.'})
                b_pdu = pickle.dumps(e_pdu)
                conn.send(b_pdu)
        elif data_type == 'O':
            menu = []
            for i in fList:
                menu.append((i.peer_name, i.file_name))
            pdu = PDU('O', menu)
            b_pdu = pickle.dumps(pdu)
            conn.send(b_pdu)
        elif data_type == 'T':
            p_peer_name = data.get('peer_name')
            p_file_name = data.get('file_name')
            found_content = False
            for d in fList:
                if d.peer_name == p_peer_name and d.file_name == p_file_name:
                    target = d
                    found_content = True
                    break
            if found_content:
                fList.remove(target)
                pdu = PDU('A', target.address)
                b_pdu = pickle.dumps(pdu)
                conn.send(b_pdu)
            else:
                e_pdu = PDU('E', {'msg': 'Record does not exists on the list.'})
                b_pdu = pickle.dumps(e_pdu)
                conn.send(b_pdu)
        elif data_type == 'Q':


            deletelist = []
            for x in fList:

                if x.peer_name == p_peer_name:
                    deletelist.append(x)

            for i in deletelist:
                fList.remove(i)


            pdu = PDU('A', "Quit")
            b_pdu = pickle.dumps(pdu)
            conn.send(b_pdu)
            s.close()
            conn.close()
            exit(0)
        # else if 'T'
        # remove the file from list
        # if file does not exist send 'E'
        # if removed successfully send 'A'

        # else if 'O'
        # iterate through the fList
        # create a list of files
        # sned the 'O' pdu, data is the list

        # else ....
        print('Done sending')

manager = Manager()
fList = manager.list()

while True:
    conn, addr = s.accept()  # Establish connection with client.
    print(addr)
    p = Process(target=service)
    p.start()
# conn.close() # close the connection
