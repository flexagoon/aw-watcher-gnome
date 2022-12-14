import argparse

from aw_core.log import setup_logging

from aw_watcher_gnome.config import parse_args
from aw_watcher_gnome.watcher import GnomeWatcher


def main() -> None:
    args = parse_args()
    setup_logging(
        "aw-watcher-gnome",
        testing=args.testing,
        log_stderr=True,
        log_file=True,
    )

    watcher = GnomeWatcher(
        poll_time=args.poll_time,
        afk_timeout=args.afk_timeout,
        testing=args.testing,
    )
    watcher.run()


if __name__ == "__main__":
    main()
