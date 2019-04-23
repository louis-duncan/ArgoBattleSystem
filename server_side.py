import os
import socket
import json
import sys
import time

WWW_DIR = ""
LISTEN_PORT = ""
with open("server_config.json", "r") as config_fh:
    config_data = json.loads(config_fh.read())
    assert type(config_data) is dict
    for k in config_data:
        locals()[k] = config_data[k]

assert "" not in (WWW_DIR, LISTEN_PORT)


class NoIPError(Exception):
    pass


def get_ip():
    name, alias_list, address_list = socket.gethostbyname_ex(socket.gethostname())
    for ip in address_list:
        if ip.startswith("10.") or ip.startswith("192.168."):
            return ip
    print("Could not find a valid local IP address.", file=sys.stderr)
    return input("Enter local IP: ")


def clear_all():
    print(time.ctime(time.time()), " - Clearing:")
    for p in os.listdir(WWW_DIR):
        if p.startswith("ship_") and p.endswith(".json"):
            print(" - ", os.path.join(WWW_DIR, p))
            with open(os.path.join(WWW_DIR, p), "w") as fh:
                fh.write(json.dumps("clear"))

    time.sleep(3)
    print(time.ctime(time.time()), " - Deleting:")
    for p in os.listdir(WWW_DIR):
        if p.startswith("ship_") and p.endswith(".json"):
            print(" - ", os.path.join(WWW_DIR, p))
            os.remove(os.path.join(WWW_DIR, p))


def worker(s):
    print(time.ctime(time.time()), " - Receiving from {}...".format(s.getpeername()))
    data = ""
    done = False
    while not done:
        b = s.recv(1)
        if b == b"":
            done = True
        else:
            data += b.decode()
    ship_name, data = json.loads(data)
    print(" - Ship:", ship_name)
    print(" - Data:", data)
    if ship_name == "" and data == "reset":
        clear_all()
        return
    file_name = os.path.join(WWW_DIR, "ship_{}.json".format(ship_name))
    with open(file_name, "w") as fh:
        fh.write(json.dumps(data))
    print(time.ctime(time.time()), " - Saved to", file_name)


def main():
    ip = get_ip()
    ss = socket.socket()
    ss.bind((ip, LISTEN_PORT))
    ss.listen(5)
    print(time.ctime(time.time()), " - Server started!")
    print(time.ctime(time.time()), " - Listening on", ip, "-", LISTEN_PORT)
    while True:
        try:
            worker(ss.accept()[0])
        except ConnectionError:
            pass


main()
