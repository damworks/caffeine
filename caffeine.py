#!/usr/bin/env python3
"""
Caffeine - Keep your system awake (Linux version)
"""

import signal
import sys
import os
import fcntl
from pathlib import Path
import pyautogui

try:
    import gi

    gi.require_version('Gtk', '3.0')
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import Gtk, GLib, AyatanaAppIndicator3 as AppIndicator3
except (ImportError, ValueError) as e:
    print("ERROR: Missing dependencies!")
    print("Install: sudo apt install python3-gi gir1.2-ayatanaappindicator3-0.1")
    sys.exit(1)

from wakepy import keep


class SingleInstance:
    def __init__(self, lockfile):
        self.lockfile = lockfile
        self.fp = None

    def __enter__(self):
        self.fp = open(self.lockfile, 'w')
        try:
            fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            print("Caffeine is already running!")
            sys.exit(1)
        return self

    def __exit__(self, *args):
        if self.fp:
            fcntl.lockf(self.fp, fcntl.LOCK_UN)
            self.fp.close()


class CaffeineApp:
    def __init__(self):
        self.active = False
        self.mode = None

        self.mouse_timer_id = None  # Set the timer

        # Get icon directory (same folder as script)
        self.icon_dir = Path(__file__).parent / "icons"

        # Check if icons exist
        if not self.icon_dir.exists():
            print(f"ERROR: Icons directory not found: {self.icon_dir}")
            print("Please create an 'icons' folder with your SVG files")
            sys.exit(1)

        icon_off = self.icon_dir / "my-caffeine-off.svg"
        icon_on = self.icon_dir / "my-caffeine-on.svg"

        if not icon_off.exists() or not icon_on.exists():
            print(f"ERROR: Icon files not found in {self.icon_dir}")
            print("Required files:")
            print("  - my-caffeine-off.svg")
            print("  - my-caffeine-on.svg")
            sys.exit(1)

        # Create indicator with custom icon path
        # Use icon name WITHOUT extension
        self.indicator = AppIndicator3.Indicator.new_with_path(
            "caffeine-app",
            "my-caffeine-off",  # without extension
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
            str(self.icon_dir)  # Path to the icons directory
        )

        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.build_menu()

    def build_menu(self):
        menu = Gtk.Menu()

        self.status_item = Gtk.MenuItem(label="☕ Inactive")
        self.status_item.set_sensitive(False)
        menu.append(self.status_item)

        menu.append(Gtk.SeparatorMenuItem())

        self.toggle_item = Gtk.MenuItem(label="Activate")
        self.toggle_item.connect("activate", self.on_toggle)
        menu.append(self.toggle_item)

        menu.append(Gtk.SeparatorMenuItem())

        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.on_quit)
        menu.append(quit_item)

        menu.show_all()
        self.indicator.set_menu(menu)

    def on_toggle(self, widget):
        if self.active:
            self.deactivate()
        else:
            self.activate()

    def simulate_activity(self):
        """Move the mouse 1 pixel forwards and backwards"""
        if not self.active:
            return False  # Stop the timer if deactivated

        try:
            x, y = pyautogui.position()
            pyautogui.moveTo(x + 1, y)
            pyautogui.moveTo(x, y)
            print("🖱️  Mouse movement")
        except Exception as e:
            print(f"⚠️  Mouse movement error: {e}")

        return True  # Continua il timer

    def activate(self):
        try:
            self.mode = keep.running()
            self.mode.__enter__()
            self.active = True

            # Start mouse movement every 4 minutes
            self.mouse_timer_id = GLib.timeout_add_seconds(
                240,
                self.simulate_activity
            )

            self.update_ui()
            print("✅ Caffeine ACTIVATED")
        except Exception as e:
            print(f"❌ Error: {e}")
            self.active = False
            self.mode = None

    def deactivate(self):
        # Stop the timer if active
        if self.mouse_timer_id:
            GLib.source_remove(self.mouse_timer_id)
            self.mouse_timer_id = None

        if self.mode:
            try:
                self.mode.__exit__(None, None, None)
                print("✅ Caffeine DEACTIVATED")
            except:
                pass
            self.mode = None
        self.active = False
        self.update_ui()

    def update_ui(self):
        if self.active:
            self.indicator.set_icon_full("my-caffeine-on", "Active")
            self.status_item.set_label("♨ ACTIVE")
            self.toggle_item.set_label("Deactivate")
        else:
            self.indicator.set_icon_full("my-caffeine-off", "Inactive")
            self.status_item.set_label("☕ Inactive")
            self.toggle_item.set_label("Activate")

    def on_quit(self, widget):
        print("👋 Shutting down...")
        self.deactivate()
        Gtk.main_quit()

    def auto_activate(self):
        self.activate()
        return False

    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        print("=" * 60)
        print("☕ Caffeine Started!")
        print("=" * 60)
        print(f"Using icons from: {self.icon_dir}")
        print("=" * 60)

        GLib.timeout_add(100, self.auto_activate)
        Gtk.main()


def main():
    lockfile = f"/tmp/caffeine-{os.getuid()}.lock"
    with SingleInstance(lockfile):
        app = CaffeineApp()
        app.run()


if __name__ == '__main__':
    main()
