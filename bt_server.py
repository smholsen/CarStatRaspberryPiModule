from bluetooth import *
import json
import time

UUID = "00000000-0000-1000-8000-00805F9B34FB"

server_sock = None
port = None

json_data = {
    "timestamp": 0,
    "speedValue": 0,
    "fuelConsumption": 0,
    "distance": 0,
    "friction": {
        "wet": 0,
        "dry": 0,
        "snow": 0,
        "ice": 0
    }
}


# Converts between dataset names and data
def get_json_name_from_data(data):
    return {
        'fuel_consumed_since_restart': 'fuelConsumption',
        'vehicle_speed': 'speedValue',
        'odometer': 'distance',
    }.get(data, 'Empty')


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


def update_json_data(data):
    global json_data

    dataset_name = get_json_name_from_data(data['name'])
    json_data["timestamp"] = data['timestamp']

    if dataset_name in json_data:
        json_data[dataset_name] = data['value']

        if dataset_name == "speedValue":
            json_data["friction"]["wet"] = breaking_distance(data['value'], 0.4)
            json_data["friction"]["dry"] = breaking_distance(data['value'], 0.9)
            json_data["friction"]["snow"] = breaking_distance(data['value'], 0.2)
            json_data["friction"]["ice"] = breaking_distance(data['value'], 0.15)


def breaking_distance(speed, c):
    return ((speed * 0.277)**2) / (2 * c * 9.81)


# Read JSON data
def send_json_data(socket=None):
    global json_data

    with open('/home/pi/Projects/carStatNewer/Border_Roads.json', 'r+') as file:
        for line in file:
            data = json.loads(line)
            update_json_data(data)
            updated_json = json.dumps(json_data)
            send_message(socket, updated_json)
            time.sleep(0.01)


# Securely close the socket
def close(client_socket):
    global server_sock

    client_socket.close()
    server_sock.close()


def run():
    client_socket = init("BluetoothServer")
    send_json_data(client_socket)
    close(client_socket)
    print("Program shut down gracefully")


if __name__ == "__main__":
    while True:
        try:
            run()
        except BluetoothError:
            print("Connection reset by peer")

