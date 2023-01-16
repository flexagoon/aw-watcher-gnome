import logging
import json
from datetime import datetime, timezone, timedelta
from time import sleep
from typing import Dict

import gi
from aw_core.models import Event
from aw_client import ActivityWatchClient
from pydbus import SessionBus

from aw_watcher_gnome.windows import get_window

logger = logging.getLogger(__name__)

td1ms = timedelta(milliseconds=1)


class GnomeWatcher:
    def __init__(self, poll_time: int, afk_timeout: int, testing: bool = False):
        self.poll_time = poll_time
        self.afk_timeout = afk_timeout

        self.client = ActivityWatchClient("aw-watcher-gnome", testing=testing)
        self.window_bucket_id = "{}_{}".format(
            "aw-watcher-window", self.client.client_hostname
        )
        self.afk_bucket_id = "{}_{}".format(
            "aw-watcher-afk", self.client.client_hostname
        )

        self.afk = False

        sb = SessionBus()
        try:
            self.FocusedWindow = sb.get(
                "org.gnome.Shell", "/org/gnome/shell/extensions/FocusedWindow"
            )
        except:
            raise Exception(
                "Failed to connect to FocusedWindow D-Bus. Do you have the extension installed?"
            )
        try:
            self.IdleMonitor = sb.get(
                "org.gnome.Mutter.IdleMonitor", "/org/gnome/Mutter/IdleMonitor/Core"
            )
        except:
            raise Exception(
                "Failed to connect to Mutter IdleMonitor D-Bus. Are you using GNOME?"
            )

    def run(self):
        logger.info("aw-watcher-gnome started")

        self.client.create_bucket(
            self.window_bucket_id, event_type="currentwindow", queued=True
        )
        self.client.create_bucket(
            self.afk_bucket_id, event_type="afkstatus", queued=True
        )

        sleep(1)

        with self.client:
            self.heartbeat_loop()

    def send_window_heartbeat(self, window: Dict[str, str]):
        window_event = Event(timestamp=datetime.now(timezone.utc), data=window)
        self.client.heartbeat(
            self.window_bucket_id,
            window_event,
            pulsetime=self.poll_time + 1,
            queued=True,
        )

    def afk_ping(self, timestamp: datetime, duration: float = 0):
        data = {"status": "afk" if self.afk else "not-afk"}
        event = Event(timestamp=timestamp, duration=duration, data=data)
        pulsetime = self.afk_timeout + self.poll_time
        self.client.heartbeat(
            self.afk_bucket_id, event, pulsetime=pulsetime, queued=True
        )

    def send_afk_event(self, idle_time: int):
        now = datetime.now(timezone.utc)
        idle_time_sec = idle_time // 1000
        last_input = now - timedelta(seconds=idle_time_sec)
        if self.afk and idle_time_sec < self.afk_timeout:
            logger.info("No longer AFK")
            self.afk_ping(timestamp=last_input)
            self.afk = False
            self.afk_ping(timestamp=last_input + td1ms)
        elif not self.afk and idle_time_sec >= self.afk_timeout:
            logger.info("Going AFK")
            self.afk_ping(timestamp=last_input)
            self.afk = True
            self.afk_ping(timestamp=last_input + td1ms, duration=idle_time_sec)
        else:
            if self.afk:
                self.afk_ping(timestamp=last_input, duration=idle_time_sec)
            else:
                self.afk_ping(timestamp=last_input)

    def heartbeat_loop(self):
        last_input_before_sleep = None
        while True:
            try:
                try:
                    window_data = json.loads(self.FocusedWindow.Get())
                except gi.repository.GLib.GError:
                    if last_input_before_sleep == None:
                        idle_time = self.IdleMonitor.GetIdletime() // 1000
                        last_input_before_sleep = datetime.now(
                            timezone.utc
                        ) - timedelta(seconds=idle_time)
                        logger.info("Computer is sleeping")
                else:
                    window = get_window(window_data)
                    self.send_window_heartbeat(window)
                    if last_input_before_sleep != None:
                        idle_time = (
                            datetime.now(timezone.utc) - last_input_before_sleep
                        ).seconds * 1000
                        last_input_before_sleep = None
                        logger.info("Computer is no longer")
                    else:
                        idle_time = self.IdleMonitor.GetIdletime()
                    self.send_afk_event(idle_time)
                finally:
                    sleep(self.poll_time)
            except KeyboardInterrupt:
                logger.info("aw-watcher-gnome stopped by keyboard interrupt")
                break
