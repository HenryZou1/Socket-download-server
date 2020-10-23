from collections import namedtuple
import pickle

############ To convert PDU object to binary format and change it back to original form
### Example:
# convert to binary
PDU = namedtuple('PDU', ['data_type', 'data'])
pdu = PDU('C', 'test.txt')
print('Original PDU:', pdu)
binary_pdu = pickle.dumps(pdu)
# change back to original
PDU = namedtuple('PDU', ['data_type', 'data'])
pdu = pickle.loads(binary_pdu)
print('Received PDU:', pdu)
###################################


############ Dictionary for the data payload
'''
The data inside PDU is different based on the types, it might be a 3part info for file registration
Or a list for the 'O' type or just a message for the 'E' type
Therefore, we need to create a universal object that can handle different situations.
We will use dictionary here to handle different type of payload. In dictionary, the data is stored in key-value basis.
Example:
a = {'key':value}
a.get('key') => value
We can have access to the values by calling their keys.
Also we can list the keys or iterate through the values in Python.
Here is an example of using dictionary for the pdu:
'''

PDU = namedtuple('PDU', ['data_type', 'data'])
pdu = PDU(data_type='R', data={'peer_name': 'Bob', 'file_name': 'test.txt', 'address': ('127.0.0.1', '36452')})

# getting the data_type
print(pdu.data_type)

# getting the peer_name
print(pdu.data.get('peer_name'))

# getting IP address of the peer address
print(pdu.data.get('address')[0])

# getting port number of the peer address
print(pdu.data.get('address')[1])

# making PDU for the 'E' type
pdu = PDU(data_type='R', data={'msg': 'This is a test!'})
print(pdu.data.get('msg'))

'''
Just make sure the dictionary keys are the same in the both sides so you can extract the data properly.
'''