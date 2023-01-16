A DBus-based ActivityWatch watcher for GNOME. It allows you to use ActivityWatch
on GNOME under Wayland.

# Prerequisites

You need the following in order to use this watcher:

- Install and set up [ActivityWatch](https://activitywatch.net)
- Install the
  [Focused Window DBus](https://github.com/flexagoon/focused-window-dbus) shell
  extension

# Installation

I currently do not provide pre-built binaries, so you'll need to compile the
project from source. You need to have `poetry` installed.

1. `poetry install`
2. `poetry run pyinstaller --clean aw-watcher-gnome.spec`
3. Copy the `dist/aw-watcher-gnome` directory to your ActivityWatch directory.
4. In the ActivityWatch config directory, open `aw-qt/aw-qt.toml`
5. In `autostart_modules`, replace `"aw-server", "aw-watcher-afk"` with
   `"aw-watcher-gnome"` (if the lines in the file are commented out, uncomment
   them)
6. Restart `aw-qt`
