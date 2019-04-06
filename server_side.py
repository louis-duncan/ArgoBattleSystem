import os
import time

WWW_DIR = "/var/www/html"


def get_valid_files(path=None, prefix="ship_", suffix=".json"):
    names = os.listdir(path)
    valid = []
    for n in names:
        if n.startswith(prefix) and n.endswith(suffix):
            valid.append(n)
    return valid


while True:
    time.sleep(1)
    file_names = get_valid_files()
    for f in file_names:
        print("Copying {} to {}...".format(f, WWW_DIR))
        with open(f, "r") as sfh:
            with open(os.path.join(WWW_DIR, f), "w") as dfh:
                dfh.write(sfh.read())
        print("Removing {}...".format(f))
        os.remove(f)
        print("Complete")
