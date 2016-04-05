#from bluetooth import *
import time
import json

UUID = "00000000-0000-1000-8000-00805F9B34FB"

server_sock = None
port = None


def send_message(message_socket, message):
    totalsent = 0
    while totalsent < len(message):
        sent = message_socket.send(message[totalsent:])
        print("Sent data: " + message[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


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


# Read JSON data
def send_json_data(socket):
    with open('Border_Roads.json', 'r+') as file:
        for line in file:
            data = json.loads(line)

            if data['name'] == 'vehicle_speed':

                # Send JSON data
                send_message(socket, line)

def send_breaking_info(socket):
    with open('Border_Roads.json', 'r+') as file:
        for line in file:
            data = json.loads(line)

            if data['name'] == 'vehicle_speed':
                # Send JSON data
                for i in range(0, 10):
                    speed = int(data['value'])
                    speed_ms = speed * 0.277

                    dry = breaking_distance(speed_ms, 0.9)
                    wet = breaking_distance(speed_ms, 0.4)
                    snow = breaking_distance(speed_ms, 0.2)
                    ice = breaking_distance(speed_ms, 0.15)

                    dictionary = {'speed_kmh' : speed, 'dry' : dry, 'wet': wet, 'snow' : snow, 'ice' : ice}

                    json_speeds = json.dumps(dictionary)

                    if i == 0:
                        send_message(socket, json_speeds)
                        print '\ntimestamp' + str(data['timestamp']) + '\nfart :' + str(speed) + '\nTorr asfalt: ' + str(dry) + '\nBlot asfalt '+ str(wet) + '\nSnofore: ' + str(snow) + '\nIsfore: ' + str(ice)

                    time.sleep(0.01)
                    i += 1

def breaking_distance(speed, koff):
    return (speed**2)/(2*koff*9.81)

# Securely close the socket
def close(client_socket):
    global server_sock

    client_socket.close()
    server_sock.close()


if __name__ == "__main__":
    client_socket = init("BluetoothServer")  #
    send_json_data(client_socket)
    close(client_socket)
    print("Program shut down successfully")
