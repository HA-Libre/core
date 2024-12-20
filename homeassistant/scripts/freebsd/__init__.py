"""Script to install/uninstall HA on FreeBSD."""

import os
import time

# mypy: allow-untyped-calls, allow-untyped-defs


def install_freebsd():
    """Set up to run via launchd on FreeBSD."""
    with os.popen("which hass") as inp:
        hass_path = inp.read().strip()

    with os.popen("whoami") as inp:
        user = inp.read().strip()

    template_path = os.path.join(os.path.dirname(__file__), "homeassistant")

    with open(template_path, encoding="utf-8") as tinp:
        rc = tinp.read()

    # rc = rc.replace("$HASS_PATH$", hass_path)
    # rc = rc.replace("$USER$", user)
    # path = os.path.expanduser("~/Library/LaunchAgents/org.homeassistant.plist")

    path = os.path.expanduser("/usr/local/etc/rc.d/homeassistant")

    try:
        with open(path, "w", encoding="utf-8") as outp:
            outp.write(rc)
    except OSError as err:
        print(f"Unable to write to {path}", err)
        return

    # os.popen(f"launchctl load -w -F {path}")

    print("Home Assistant has been installed. Open it here: http://localhost:8123")


def uninstall_freebsd():
    """Unload from launchd on OS X."""
    path = os.path.expanduser("/usr/local/etc/rc.d/homeassistant")
    # os.popen(f"launchctl unload {path}")

    print("Home Assistant has been uninstalled.")


def run(args: list[str]) -> int:
    """Handle FreeBSD commandline script."""
    commands = "install", "uninstall", "restart"
    if not args or args[0] not in commands:
        print("Invalid command. Available commands:", ", ".join(commands))
        return 1

    if args[0] == "install":
        install_freebsd()
        return 0
    if args[0] == "uninstall":
        uninstall_freebsd()
        return 0
    if args[0] == "restart":
        uninstall_freebsd()
        # A small delay is needed on some systems to let the unload finish.
        # time.sleep(0.5)
        install_freebsd()
        return 0

    raise ValueError(f"Invalid command {args[0]}")
