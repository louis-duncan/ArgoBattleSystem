import ftplib
import json
import tmp.tempfile as tf

HOST = "home.ltcomputing.co.uk"
USER = "ftp_client"
PASS = "password"


class Communicator:
    def __init__(self):
        self._ftp = ftplib.FTP()

    def _connect(self):
        self._ftp.connect(HOST)
        self._ftp.login(USER, PASS)

    def _close(self):
        self._ftp.quit()

    def _format_for_sending(self, obj):
        path = tf.mkdtemp()
        try:
            with open(path, "w") as fh:
                fh.write(json.dumps(obj))
        except json.JSONDecodeError:
            path = None
        return path

    def _ftp_upload(self, source, destination):
        self._ftp.