from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
	"""Sets up handling for incoming clients."""
	while True:
		client, client_address = SERVER.accept()
		name = client.recv(BUFSIZ).decode("utf8")
		print("%s has connected as %s." % (name, client_address))
		client.send(bytes("Greetings from the cave!", "utf8"))
		clients[client] = name
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
	"""Handles a single client connection."""
	name = clients[client]
	welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
	client.send(bytes(welcome, "utf8"))
	msg = "%s has joined the chat!" % name
	broadcast(bytes(msg, "utf8"))

	while True:
		msg = client.recv(BUFSIZ)
		if msg != bytes("{quit}", "utf8"):
			broadcast(msg, name+": ")
		else:
			quitClient(client)
			break


def quitClient(client):
	name = clients[client]
	client.send(bytes("{quit}", "utf8"))
	client.close()
	del clients[client]
	broadcast(bytes("%s has left the chat." % name, "utf8"))
	print("%s has dropped" % name)


def broadcast(msg, prefix=""):  # prefix is for name identification.
	"""Broadcasts a message to all the clients."""

	for sock in clients:
		sock.send(bytes(prefix, "utf8")+msg)


clients = {}
addresses = {}

HOST = ''
name = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
	SERVER.listen(10)
	print("Waiting for connection...")
	ACCEPT_THREAD = Thread(target=accept_incoming_connections)
	ACCEPT_THREAD.setDaemon(True)
	ACCEPT_THREAD.start()
	#ACCEPT_THREAD.join()
	while(1):
		key = input()
		if key == "{quit}":
			for cli in list(clients):
				quitClient(cli)
			SERVER.close()
			print("Exiting the server...\n")
			exit(0)
