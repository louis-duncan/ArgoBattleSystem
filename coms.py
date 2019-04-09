import ftplib
import json
import os
import random
import time

import requests
import _thread

HOST = "home.ltcomputing.co.uk"
FTP_PORT = 31416
HTTP_PORT = 31417
USER = "ftp_client"
PASS = "password"
TEMP_DIR = "tmp/"


class FTPSender:
    def __init__(self):
        self._ftp = ftplib.FTP()
        self._queue = []
        self.worker_pid = _thread.start_new(self._worker, ())

    def _connect(self):
        self._ftp.connect(HOST, FTP_PORT)
        self._ftp.login(USER, PASS)

    def _close(self):
        self._ftp.quit()

    def _format_for_sending(self, obj):
        path = os.path.join(TEMP_DIR, str(random.randint(100000, 999999)) + ".json")
        with open(path, "w") as fh:
            fh.write(json.dumps(obj))
        return path

    def _ftp_upload(self, source, destination):
        self._connect()
        with open(source, "br") as fh:
            self._ftp.storbinary("STOR {}".format(destination), fh)

    def send(self, obj, ship_name):
        self._queue.append((obj, ship_name))

    def _worker(self):
        while True:
            if len(self._queue) > 0:
                obj, ship_name = self._queue.pop(0)
                path = self._format_for_sending(obj)
                done = False
                count = 0
                while not done and count < 3:
                    count += 1
                    try:
                        self._connect()
                        self._ftp_upload(path, "ship_{}.json".format(ship_name))
                        done = True
                    except ftplib.all_errors:
                        print("Failed to send:", obj, " Attempt no:", count)
                time.sleep(0.5)
                os.remove(path)
            time.sleep(0.2)


class HTTPGetter:
    def __init__(self):
        pass

    def get(self, ship_name):
        r = requests.get("http://{}:{}/ship_{}.json".format(HOST,
                                                                HTTP_PORT,
                                                                ship_name))
        if r.status_code == 200:
            return json.loads(r.text)
        else:
            return None
