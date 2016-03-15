from bluetooth import *
from time import sleep

# DISCLAIMER - if you do not have pybluez installed there will be a lot of red lines in the following code

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id=uuid,
                   service_classes=[uuid, SERIAL_PORT_CLASS]
                    )

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)


# Right now it is receiving data - change the "sock.recv" if you want it to send
try:
    sent = 0

    while sent < 100:
        sent = client_sock.sock.send("Halla")

        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
        print totalsent

        sleep(1)

except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")

# TODO Make a file reader to read in the raw OBD2-data and send them to the bluetooth socket