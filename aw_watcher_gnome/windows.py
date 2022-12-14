import re
from typing import Dict


def get_window(window_data: Dict[str, str]) -> Dict[str, str]:
    app = window_data["wm_class"]
    title = window_data["title"]
    forced_windows = {
        "org.telegram.desktop": {
            "app": "Telegram",
            "title": "Telegram",
        },
        "Code": {
            "app": "Code",
            "title": re.sub(r"^● ", "", title),
        },
    }
    if app in forced_windows:
        return forced_windows[app]
    else:
        return {
            "app": app,
            "title": title,
        }
