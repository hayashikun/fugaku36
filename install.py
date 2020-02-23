import json
import logging
import os
import subprocess
from os import path
from urllib import request, parse

IMAGE_URL = "https://raw.githubusercontent.com/hayashikun/fugaku36/master/resouces/images/{}"
JSON_URL = "https://raw.githubusercontent.com/hayashikun/fugaku36/master/resouces/resource.json"
PY_SCRIPT_URL = "https://raw.githubusercontent.com/hayashikun/fugaku36/master/fugaku36.py"
PLIST_URL = "https://raw.githubusercontent.com/hayashikun/fugaku36/master/fugaku36.plist"

HOME_PATH = path.expanduser("~")
INSTALL_PATH = path.join(HOME_PATH, ".cache", "fugaku36")

IMAGE_PATH = path.join(INSTALL_PATH, "images")
JSON_PATH = path.join(INSTALL_PATH, "resource.json")
PY_SCRIPT_PATH = path.join(INSTALL_PATH, "fugaku36.py")
SH_SCRIPT_PATH = path.join(INSTALL_PATH, "fugaku36")
PLIST_PATH = path.join(INSTALL_PATH, "fugaku36.plist")
LAUNCH_AGENTS_PATH = path.join(HOME_PATH, "Library", "LaunchAgents", "fugaku36.plist")


def install():
    logger = logging.getLogger("fugaku36_install")
    sh = logging.StreamHandler()
    logger.addHandler(sh)
    logger.setLevel(logging.INFO)

    if not path.exists(INSTALL_PATH):
        os.makedirs(INSTALL_PATH)
    if not path.exists(IMAGE_PATH):
        os.makedirs(IMAGE_PATH)

    update_resource = False

    if path.exists(JSON_PATH):
        with open(JSON_PATH) as f:
            j = json.load(f)
            old_version = j["version"]
    else:
        old_version = 0

    request.urlretrieve(JSON_URL, JSON_PATH)
    logger.info("Image JSON file has been downloaded.")

    with open(JSON_PATH) as f:
        j = json.load(f)
        if old_version < j["version"]:
            update_resource = True
            logger.info("Resources will be updated.")

        image_names = j["images"]

    for name in image_names:
        if not update_resource and path.exists(path.join(IMAGE_PATH, name)):
            continue
        request.urlretrieve(IMAGE_URL.format(parse.quote(name)), path.join(IMAGE_PATH, name))
        logger.info("Image %s has been downloaded.", name)

    request.urlretrieve(PY_SCRIPT_URL, PY_SCRIPT_PATH)
    logger.info("Python scripts have been downloaded.")

    with open(PY_SCRIPT_PATH) as f:
        py_script = f.read()
    py_script = "#!/usr/bin/python3\n" + py_script

    with open(SH_SCRIPT_PATH, "w") as f:
        f.write(py_script)

    cmd = [
        "chmod", "a+x", SH_SCRIPT_PATH
    ]
    subprocess.run(cmd)

    cmd = [
        "ln",
        "-s",
        SH_SCRIPT_PATH,
        "/usr/local/bin/fugaku36"
    ]
    subprocess.run(cmd)
    logger.info("Symbolic link is created.")

    cmd = [
        "cp",
        PLIST_PATH,
        LAUNCH_AGENTS_PATH
    ]
    subprocess.run(cmd)

    cmd = [
        "launchctl", "load", LAUNCH_AGENTS_PATH
    ]
    subprocess.run(cmd)
    logger.info("Application is registered to launchd.")

    logger.info("fugaku36 is successfully installed!")


if __name__ == "__main__":
    install()
