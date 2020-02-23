import json
import logging
import random
import subprocess
from os import path

APP_PATH = path.join(path.expanduser("~"), ".cache", "fugaku36")
IMAGE_PATH = path.join(APP_PATH, "images")
JSON_PATH = path.join(APP_PATH, "resource.json")


def update():
    logger = logging.getLogger("fugaku36")
    sh = logging.StreamHandler()
    logger.addHandler(sh)
    logger.setLevel(logging.INFO)

    with open(JSON_PATH) as f:
        j = json.load(f)
        image_names = j["images"]

    image_path = path.join(IMAGE_PATH, random.choice(image_names))
    logger.info("Background image will be changed to %s", image_path)

    if not change_background(image_path):
        logger.error("Failed to update background image.")


def change_background(image_path):
    cmd = [
        "osascript",
        "-e",
        "tell application \"Finder\" to set desktop picture to POSIX file \"{}\"".format(image_path),
    ]
    try:
        subprocess.run(cmd)
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    update()
