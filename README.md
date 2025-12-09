# ☕ Caffeine - Keep Your Linux System Awake

A lightweight utility to prevent your Linux system from going to sleep. Features a clean system tray interface for easy control.

## ✨ Features

- 🎯 **System Tray Integration**: Clean icon interface with visual status indicators
- 🔋 **Smart Sleep Prevention**: Uses native DBus APIs and mouse movement simulation
- 🎨 **Visual Feedback**: Icons with status indicators (active/inactive)
- 🪶 **Lightweight**: Minimal resource usage
- 🔒 **Single Instance**: Prevents multiple instances from running simultaneously

## 📋 Requirements

- Python 3.10 or higher (Python 3.12 recommended for building)
- Linux with GTK3 and DBus support
- Debian-based distro (Ubuntu, Debian, Mint, etc.) recommended

### System Dependencies

#### Ubuntu/Debian
```
sudo apt install python3-gi gir1.2-ayatanaappindicator3-0.1
```

## 🚀 Installation

### 1. Clone the Repository

```
git clone https://github.com/damworks/caffeine-py.git
cd caffeine-py
```

### 2. Create Icons Directory

Create an `icons/` folder with your icon files:
- `my-caffeine-off-symbolic.svg` - Inactive state icon
- `my-caffeine-on-symbolic.svg` - Active state icon

### 2. Create a Virtual Environment (Recommended)

```
python3 -m venv venv
source venv/bin/activate
(if you're using fish)
source venv/bin/activate.fish
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

## 🎮 Usage

### Running the Application

```
python caffeine.py
```

Or make it executable:

```
chmod +x caffeine.py
./caffeine.py
```

### Using the System Tray Icon

1. **Look for the icon**: The icon will appear in your system tray
2. **Toggle activation**: Left-click the icon and select "Activate" or "Deactivate"
3. **Check status**: The menu shows current status (Active/Inactive)
4. **Quit**: Select "Quit" from the menu to exit

## 🔧 How It Works

Caffeine prevents your system from sleeping using two mechanisms:
- **wakepy library**: Uses DBus `org.freedesktop.ScreenSaver.Inhibit` to prevent sleep
- **Mouse simulation**: Moves mouse by 1 pixel every 4 minutes as additional prevention

The application also prevents multiple instances from running simultaneously using file locking.

## 🐛 Troubleshooting

### Icon doesn't appear

Ensure you have the required system packages:

```
sudo apt install gir1.2-appindicator3-0.1
```

### Icons not found error

Make sure you have created the `icons/` directory with the required SVG files in the same folder as `caffeine.py`.

### Permission Issues

Ensure your user has access to DBus and check group membership:

```
# Check if you're in the required groups
groups
```
# Should include: audio, video, plugdev (varies by distro)

## 📦 Building a Standalone Executable

To create a standalone executable, you need PyInstaller installed **in the virtual environment**:

### Activate your virtual environment first
```
source venv/bin/activate
```

### Install PyInstaller in the venv
```
pip install --ignore-installed pyinstaller
```

### Build the executable
(./venv/bin/pyinstaller)
```
pyinstaller --onefile --windowed --name=Caffeine \
  --add-data "icons:icons" \
  --hidden-import=pyautogui \
  --hidden-import=wakepy \
  --hidden-import=Xlib \
  caffeine.py
```

The executable will be in the `dist/` folder and can run without Python installed.

**Important Notes:**
- Always use the PyInstaller from your venv (`./venv/bin/pyinstaller`)
- If you encounter issues with Python 3.13, use Python 3.12 for building
- The executable runs without opening a terminal window

### Making it Available Globally

Copy the executable to system path
```
sudo cp dist/Caffeine /usr/local/bin/
```

Now you can run it from anywhere
```
Caffeine
```

### Creating a Desktop Icon and Making Caffeine Available in the Application Menu

1. Copy the Executable
```
sudo cp dist/Caffeine /usr/local/bin/caffeine
sudo chmod +x /usr/local/bin/caffeine
```

2. Copy the Icon
```
# Create the directory for app icons
sudo mkdir -p /usr/share/icons/hicolor/scalable/apps

# Copy the icon
sudo cp icons/coffee-to.go.svg /usr/share/icons/hicolor/scalable/apps/
```

3. Create the Desktop Entry
Create the `.desktop` file:
```
sudo nano /usr/share/applications/caffeine.desktop
```

Insert this content:
```
[Desktop Entry]
Version=1.0
Type=Application
Name=Caffeine
Comment=Prevent your system from going to sleep
Icon=coffee-to-go
Exec=/usr/local/bin/caffeine
Terminal=false
Categories=Utility;System;
Keywords=caffeine;sleep;awake;screensaver;
StartupNotify=false
```

4. Update the Icon Cache
```
sudo update-desktop-database /usr/share/applications
sudo gtk-update-icon-cache /usr/share/icons/hicolor -f
```

**Final Structure:**
```
/usr/local/bin/caffeine                                 # Executable
/usr/share/icons/hicolor/scalable/apps/coffee-to-go.svg # Icon
~/.local/share/applications/caffeine.desktop            # Desktop entry
```

After these steps, search for "Caffeine" in your application menu - it should appear in the "System Tools" category.


## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Credits

Built with:
- [wakepy](https://github.com/fohrloop/wakepy) - Cross-platform sleep prevention
- [PyGObject](https://pygobject.readthedocs.io/) - GTK3 bindings for Python
- [pyautogui](https://github.com/asweigart/pyautogui) - Mouse automation

## 📝 Changelog

### Version 1.0.0
- Initial Linux release
- System tray integration with AyatanaAppIndicator3
- Dual prevention mechanism (wakepy + mouse simulation)
- Single instance lock
- Auto-activation on startup