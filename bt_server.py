from bluetooth import *
from time import sleep

# DISCLAIMER - if you do not have pybluez installed there will be a lot of red lines in the following code
def send_message(message_socket, message):
    totalsent = 0
    while totalsent < len(message):
        sent = message_socket.send(message[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "00000000-0000-1000-8000-00805F9B34FB"

advertise_service( server_sock, "SampleServer",
                   service_id=uuid,
                   service_classes=[uuid, SERIAL_PORT_CLASS]
                    )

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

send_message(client_sock, "Hello Moto!\n")

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")

# TODO Make a file reader to read in the raw OBD2-data and send them to the bluetooth socket
