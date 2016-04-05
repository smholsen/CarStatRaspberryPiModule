from bluetooth import *
from time import sleep

UUID = "00000000-0000-1000-8000-00805F9B34FB"

server_sock = None
port = None


def send_message(message_socket, message):
    totalsent = 0
    while totalsent < len(message):
        sent = message_socket.send(message[totalsent:])
        print "Sent: " + message[totalsent:]
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


# Unpack the JSON object and send it
def send_json(socket, json_obj):
    data = json_obj

    send_message(socket, data)


# Initialize data connection
def init(name):
    global server_sock
    global port

    server_sock = BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    advertise_service( server_sock, name,
                   service_id=UUID,
                   service_classes=[UUID, SERIAL_PORT_CLASS])

    print("Waiting for connection on RFCOMM channel %d" % port)
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)
    return client_sock


def close(client_socket):
    global server_sock

    client_socket.close()
    server_sock.close()



if __name__ == "__main__":
    client_socket = init("BluetoothServer")  #


    close(client_socket)
    print("Program shut down successfully")

# TODO Make a file reader to read in the raw OBD2-data and send them to the bluetooth socket
