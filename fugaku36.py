import argparse
import json
import logging
import random
import subprocess
from os import path
from datetime import datetime

APP_PATH = path.join(path.expanduser("~"), ".cache", "fugaku36")
IMAGE_PATH = path.join(APP_PATH, "images")
JSON_PATH = path.join(APP_PATH, "resource.json")
UPDATE_LOG_PATH = path.join(APP_PATH, "update.log")


def update(log_level=logging.ERROR, update_period=0):
    logger = logging.getLogger("fugaku36")
    sh = logging.StreamHandler()
    logger.addHandler(sh)
    logger.setLevel(log_level)

    last_image = None
    if update_period > 0 and path.exists(UPDATE_LOG_PATH):
        with open(UPDATE_LOG_PATH) as f:
            logs = f.read().split("\t")
            last_update = datetime.fromisoformat(logs[0])
            if (datetime.now() - last_update).total_seconds() < update_period * 3600:
                logger.info("Background is not updated.")
                return
            last_image = logs[1]

    with open(JSON_PATH) as f:
        j = json.load(f)
        image_names = j["images"]

    if last_image is not None:
        image_names.remove(last_image.strip())

    image = random.choice(image_names)
    image_path = path.join(IMAGE_PATH, image)
    logger.info("Background image will be changed to %s", image)

    if change_background(image_path):
        with open(UPDATE_LOG_PATH, "w") as f:
            f.write("\t".join([datetime.now().isoformat(), image]))
    else:
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
    parser = argparse.ArgumentParser(description="Fugaku36")
    parser.add_argument("--update_period", type=int, default=0, help="Update period.")
    parser.add_argument("--verbose", action="store_true", help="Make the output more detail.")

    args = parser.parse_args()

    level = logging.ERROR
    if args.verbose:
        level = logging.INFO

    update(level, args.update_period)
