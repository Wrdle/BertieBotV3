import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

print("Sending request…")
socket.send(b'ALLCHaNNELS FROM {SERVER ID}')

#  Get the reply.
message = socket.recv()
print("Received reply %s" % message)

print("Sending request…")
socket.send(b'SPECIFICCHANNEL')

#  Get the reply.
message = socket.recv()
print("Received reply %s" % message)

print("Sending request…")
socket.send(b'user')

#  Get the reply.
message = socket.recv()
print("Received reply %s" % message)

print("Sending request…")
socket.send(b'ROLE')

#  Get the reply.
message = socket.recv()
print("Received reply %s" % message)