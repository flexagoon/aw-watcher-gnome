A DBus-based ActivityWatch watcher for GNOME. It allows you to use ActivityWatch
on GNOME under Wayland.

# Prerequisites

You need the following in order to use this watcher:

- Install and set up [ActivityWatch](https://activitywatch.net)
- Install the
  [Focused Window DBus](https://extensions.gnome.org/extension/5592/focused-window-d-bus)
  shell extension

# Installation

I currently do not provide pre-built binaries, so you'll need to compile the
project from source. You need to have `poetry` installed.

1. `poetry install`
2. `poetry run pyinstaller --clean aw-watcher-gnome.spec`
3. Copy the `dist/aw-watcher-gnome` directory to your ActivityWatch directory.

# Usage

## With aq-qt
1. In the ActivityWatch config directory, open `aw-qt/aw-qt.toml`
2. In `autostart_modules`, replace `"aw-watcher-afk", "aw-watcher-window"` with
   `"aw-watcher-gnome"` (if the lines in the file are commented out, uncomment
   them)
3. Restart `aw-qt`, or alternatively 

# Manually without aw-qt
1. Follow 
   [upstream docs for running on GNOME](https://docs.activitywatch.net/en/latest/running-on-gnome.html#running-on-gnome),
   but use `./aw-watcher-gnome/aw-watcher-gnome &` instead of `aw-watcher-afk` and 
   `aw-watcher-window`)
