import ftplib
import json
import os
import random
import requests
import _thread

HOST = "home.ltcomputing.co.uk"
FTP_PORT = 31416
HTTP_PORT = 31417
USER = "ftp_client"
PASS = "password"


class FTPSender:
    def __init__(self):
        self._ftp = ftplib.FTP()

    def _connect(self):
        self._ftp.connect(HOST, FTP_PORT)
        self._ftp.login(USER, PASS)

    def _close(self):
        self._ftp.quit()

    def _format_for_sending(self, obj):
        path = str(random.randint(100000, 999999)) + ".json"
        try:
            with open(path, "w") as fh:
                fh.write(json.dumps(obj))
        except json.JSONDecodeError:
            path = None
        return path

    def _ftp_upload(self, source, destination):
        self._connect()
        with open(source, "br") as fh:
            self._ftp.storbinary("STOR {}".format(destination), fh)
        self._close()

    def send(self, obj, ship_name, threaded=True):
        if threaded:
            _thread.start_new(self.send, (obj, ship_name, False))
            return
        path = self._format_for_sending(obj)
        self._connect()
        self._ftp_upload(path, "ship_{}.json".format(ship_name))
        os.remove(path)


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
