# HeadsetControl GUI

A modern graphical user interface for [HeadsetControl](https://github.com/Sapd/HeadsetControl) with dark/light theme support and multi-language interface (English/Polish).

![HeadsetControl GUI Dark Theme](https://img.shields.io/badge/Theme-Dark%20%2F%20Light-blue)
![Python](https://img.shields.io/badge/Python-3.7%2B-green)
![Platform](https://img.shields.io/badge/Platform-Linux-orange)
![License](https://img.shields.io/badge/License-MIT-red)

## Features

✨ **Modern GUI Interface**
- Clean, intuitive design with tkinter
- Dark and light theme support
- Responsive layout with proper spacing

🌐 **Multi-language Support**
- English and Polish interface
- Easy language switching
- Automatic configuration saving

🎛️ **Comprehensive Controls**
- Device selection (vendorid:productid)
- Sidetone level adjustment (0-128)
- Equalizer preset selection (0-3)
- Lights control (On/Off)
- Voice prompts control (On/Off)
- Microphone mute control (On/Off)
- Battery level checking

💾 **Settings Persistence**
- Automatically saves language and theme preferences
- Restores last used settings on startup
- Configuration stored in JSON format

## Requirements

### System Requirements
- **Operating System**: Linux (tested on Ubuntu/Kubuntu)
- **Python**: 3.7 or higher
- **HeadsetControl**: Must be installed and accessible via command line

### Python Dependencies
- `tkinter` (usually included with Python)
- `subprocess` (built-in)
- `json` (built-in)
- `os` (built-in)

## Installation

### 1. Install HeadsetControl

First, you need to install HeadsetControl on your system:

#### Option A: From Package Manager (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install headsetcontrol
```

#### Option B: From Source
```bash
# Install dependencies
sudo apt install build-essential cmake libhidapi-dev

# Clone and build HeadsetControl
git clone https://github.com/Sapd/HeadsetControl.git
cd HeadsetControl
mkdir build && cd build
cmake ..
make
sudo make install
```

### 2. Install Python Dependencies

#### Install tkinter (if not already installed)
```bash
sudo apt install python3-tk
```

#### Verify HeadsetControl installation
```bash
headsetcontrol --help
```

### 3. Download and Run GUI

#### Option A: Clone this repository
```bash
git clone https://github.com/JanDziaslo/headsetcontrol-gui.git
cd headsetcontrol-gui
python3 headsetcontrolGUI.py
```

#### Option B: Download single file
```bash
wget https://raw.githubusercontent.com/JanDziaslo/headsetcontrol-gui/main/headsetcontrolGUI.py
python3 headsetcontrolGUI.py
```

## Usage

### Basic Operation

1. **Launch the application**:
   ```bash
   python3 headsetcontrolGUI.py
   ```

2. **Select your language** (English/Polish) from the dropdown

3. **Choose theme** (Dark/Light) - Dark theme is default

4. **Configure device** (optional):
   - Enter your device ID in format `vendorid:productid`
   - Leave empty to use default device

5. **Adjust settings**:
   - **Sidetone**: Use slider to set level (0-128)
   - **Equalizer**: Choose preset (0-3)
   - **Lights**: Turn headset lights On/Off
   - **Voice Prompts**: Enable/disable voice notifications
   - **Mic Mute**: Control microphone mute function

6. **Apply settings**: Click "Apply Settings" to send commands to headset

7. **Check battery**: Click "Check Battery" to see current battery level

### Advanced Usage

#### Finding Your Device ID
```bash
headsetcontrol -?
# Look for your device in the output and note the vendor:product ID
```

#### Command Line Equivalent
The GUI generates commands equivalent to:
```bash
# Examples:
headsetcontrol -s 64              # Set sidetone to 64
headsetcontrol -l 1               # Turn lights on
headsetcontrol -b                 # Check battery
headsetcontrol -d 1234:5678 -s 32 # Use specific device and set sidetone
```

## Configuration

The application automatically creates a configuration file `headsetcontrol_config.json` in the same directory to store your preferences:

```json
{
  "language": "en",
  "theme": "dark"
}
```

You can manually edit this file or use the GUI controls to change settings.

## Supported Devices

This GUI works with any headset supported by HeadsetControl. Popular supported devices include:

- SteelSeries Arctis series (7, 9, Pro, etc.)
- Corsair Void series
- Logitech G series (G933, G935, etc.)
- HyperX Cloud series
- And many more...

For a complete list, check the [HeadsetControl documentation](https://github.com/Sapd/HeadsetControl#supported-headsets).

## Troubleshooting

### Common Issues

#### "headsetcontrol: command not found"
```bash
# Install HeadsetControl first
sudo apt install headsetcontrol
# OR build from source (see installation section)
```

#### "ModuleNotFoundError: No module named 'tkinter'"
```bash
# Install tkinter
sudo apt install python3-tk
```

#### "No headset found"
- Make sure your headset is connected
- Try running `headsetcontrol -?` to see if your device is detected
- Check if you need specific device ID with `-d vendorid:productid`

#### Permission Issues
```bash
# You might need to add your user to appropriate groups
sudo usermod -a -G audio $USER
sudo usermod -a -G input $USER
# Logout and login again
```

### Device-Specific Issues

#### Device requires specific vendor:product ID
1. Run `headsetcontrol -?` to find your device
2. Use the format shown in the output (e.g., `1038:12ad`)
3. Enter this in the "Device" field in the GUI

#### Features not working
- Not all features are supported by all devices
- Check HeadsetControl documentation for your specific model
- Some features may require firmware updates

## Development

### Running from Source
```bash
git clone https://github.com/JanDziaslo/headsetcontrol-gui.git
cd headsetcontrol-gui
python3 headsetcontrolGUI.py
```

### Adding New Languages
1. Edit the `LANGUAGES` dictionary in `headsetcontrolGUI.py`
2. Add your language code and translations
3. Update the language combo box values

### Contributing
Pull requests are welcome! Please ensure:
- Code follows Python best practices
- Test on different Linux distributions
- Update documentation as needed

## Testing

**Note**: This application has been tested only on Linux systems (Ubuntu/Kubuntu). While it should work on other Unix-like systems, Windows compatibility has not been tested.

### Tested On
- Ubuntu 20.04, 22.04, 24.04
- Kubuntu 24.10
- Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13

### Test Your Setup
```bash
# Test HeadsetControl
headsetcontrol -b

# Test GUI
python3 headsetcontrolGUI.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- **HeadsetControl**: [Sapd/HeadsetControl](https://github.com/Sapd/HeadsetControl) - The core functionality
- **GUI Development**: Created with Python tkinter
- **Testing**: Community feedback and testing on various Linux distributions

## Support

If you encounter issues:

1. Check this README for troubleshooting steps
2. Verify HeadsetControl works independently: `headsetcontrol -b`
3. Open an issue on GitHub with:
   - Your Linux distribution and version
   - Python version (`python3 --version`)
   - HeadsetControl version (`headsetcontrol --version`)
   - Complete error message
   - Your headset model

## Changelog

### v1.0.0
- Initial release
- Dark/Light theme support
- English/Polish language support
- Core HeadsetControl functionality
- Settings persistence
- Linux compatibility tested
