import argparse

from aw_core.config import load_config_toml

default_config = """
[aw-watcher-gnome]
afk_timeout = 180
poll_time = 1
"""


def load_config():
    return load_config_toml("aw-watcher-gnome", default_config)["aw-watcher-gnome"]


def parse_args():
    config = load_config()

    default_poll_time = config["poll_time"]
    default_afk_timeout = config["afk_timeout"]

    parser = argparse.ArgumentParser(
        "A DBus-based window+afk watcher for ActivityWatch and GNOME"
    )
    parser.add_argument("--testing", dest="testing", action="store_true")
    parser.add_argument(
        "-p",
        "--poll-time",
        dest="poll_time",
        type=int,
        default=default_poll_time,
        help="time between sending updates to the server",
    )
    parser.add_argument(
        "-a",
        "--afk-timeout",
        dest="afk_timeout",
        type=int,
        default=default_afk_timeout,
        help="seconds before last input to mark you as afk",
    )
    return parser.parse_args()
