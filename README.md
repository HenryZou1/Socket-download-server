# Socket-download-server
Socket based python download server with fork (linux)
This program was test in a linux environment does not work with windows. This program works within the local area network and works like a torrent program. This application has two components a client and a server. The server component listens to connection from multiple client and services them when needed. The client listens for incoming connections from other clients and run user commands at the same time with python's multiprocessing api. Clients register their socket location, and file name to the server database. When the client wants to download from application, it makes a request to the server which will return the socket location of the given file. It will then download the file from the other client's socket directly.
