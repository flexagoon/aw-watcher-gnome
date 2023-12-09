# WARNING

This watcher is no longer maintained. It probably still works, But I'll no longer fix it if it breaks. It is recommended to use [awatcher](https://github.com/2e3s/awatcher) instead.

---

<details>
<summary>Previous readme</summary>

# aw-watcher-gnome

A DBus-based ActivityWatch watcher for GNOME. It allows you to use ActivityWatch
on GNOME under Wayland.

## Prerequisites

You need the following in order to use this watcher:

- Install and set up [ActivityWatch](https://activitywatch.net)
- Install the
  [Focused Window DBus](https://extensions.gnome.org/extension/5592/focused-window-d-bus)
  shell extension

## Installation

I currently do not provide pre-built binaries, so you'll need to compile the
project from source. You need to have `poetry` installed.

1. `poetry install`
2. `poetry run pyinstaller --clean aw-watcher-gnome.spec`
3. Copy the `dist/aw-watcher-gnome` directory to your ActivityWatch directory.

## Autostart

### With aw-qt

1. In the ActivityWatch config directory, open `aw-qt/aw-qt.toml`
2. In `autostart_modules`, replace `"aw-server", "aw-watcher-afk"` with
   `"aw-watcher-gnome"` (if the lines in the file are commented out, uncomment
   them)
3. Restart `aw-qt`

### With systemd

1. Disable aw-qt or any other autostart methods, if they are enabled
2. Copy the services from the
   [systemd](https://github.com/flexagoon/aw-watcher-gnome/tree/main/systemd)
   directory to `~/.local/share/systemd/user`
3. Run
   `systemctl enable --user --now aw-server && systemctl enable --user --now aw-watcher-gnome`

</details>
