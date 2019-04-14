import socket
import json
import time

import requests
import _thread

HOST = "home.ltcomputing.co.uk"
UPLOAD_PORT = 31416
HTTP_PORT = 31417

TEMP_DIR = "tmp/"


class Sender:
    def __init__(self):
        self._queue = []
        self.worker_pid = _thread.start_new(self._worker, ())

    def send(self, ship_name, obj):
        self._queue.append((ship_name, obj))

    def _worker(self):
        while True:
            for q in self._queue:
                s = socket.socket()
                s.connect((HOST, UPLOAD_PORT))
                s.send(json.dumps(q).encode())
                s.close()
            self._queue.clear()
            time.sleep(0.1)


class HTTPGetter:
    def __init__(self):
        pass

    def get(self, ship_name):
        r = requests.get("http://{}:{}/ship_{}.json".format(HOST,
                                                            HTTP_PORT,
                                                            ship_name))
        if r.status_code == 200:
            try:
                return json.loads(r.text)
            except json.JSONDecodeError:
                return list()
        else:
            return list()
