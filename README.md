# KDE Plasma Backup Manager

[![GitHub](https://img.shields.io/badge/github-alduccino/KDE--Plasma--Backup--Manager-blue?logo=github)](https://github.com/alduccino/KDE-Plasma-Backup-Manager)
[![Platform](https://img.shields.io/badge/platform-Fedora%20Linux-51A2DA?logo=fedora)](https://fedoraproject.org/)
[![KDE Plasma](https://img.shields.io/badge/KDE%20Plasma-6.5%2B-1D99F3?logo=kde)](https://kde.org/plasma-desktop/)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python)](https://www.python.org/)
[![Qt](https://img.shields.io/badge/Qt-6-41CD52?logo=qt)](https://www.qt.io/)
[![License](https://img.shields.io/badge/license-GPL--3.0-green)](LICENSE)

A comprehensive Qt6-based backup and restore solution for KDE Plasma systems, specifically designed for Fedora Linux with KDE Plasma 6.5+.

---

---

## Screenshots

### Main Backup Interface
![Backup Tab](docs/images/backup-tab.png)
*Simple and intuitive backup interface with progress tracking*

### Restore Interface
![Restore Tab](docs/images/restore-tab.png)
*Easy restore with backup browsing and safety warnings*

### Settings & Info
![Settings Tab](docs/images/settings-tab.png)
*System information and configuration*

> **Note:** Screenshots coming soon! Feel free to contribute screenshots from your system.

---

## Features

### What Gets Backed Up

✅ **KDE Plasma Settings**
- All Plasma configuration files
- Plasmoid (widget) configurations and settings
- Desktop layouts and panel configurations
- Keyboard shortcuts and hotkeys
- Display and window manager settings
- Konsole profiles and color schemes
- System tray settings

✅ **Application Configurations**
- Complete Firefox profiles (bookmarks, extensions, settings)
- Complete Thunderbird profiles (emails, accounts, filters)
- General application configurations from ~/.config
- Application data from ~/.local/share
- Shell configurations (.bashrc, .zshrc, etc.)
- Git configuration
- SSH configuration
- VS Code/Codium settings

✅ **User Directories**
- Documents (or localized name like "Documents" in French)
- Pictures/Images (or "Images" in French)
- Videos/Vidéos (or "Vidéos" in French)
- Music/Musique
- Downloads/Téléchargements
- Automatically detects XDG user directory names (supports all languages)

### Key Features

- 🎨 **Native Qt6 Interface** - Fully integrated with KDE Plasma 6.5+
- 🌐 **NAS Integration** - Designed for network storage backup
- 🏷️ **Per-Host Backups** - Automatically organizes backups by hostname
- 📅 **Timestamped Backups** - Each backup includes timestamp for easy identification
- 🔄 **Complete Restore** - One-click restoration of all settings
- 🌍 **Localization Support** - Handles localized directory names (French, etc.)
- 📊 **Progress Tracking** - Real-time progress updates during backup/restore
- 💾 **Metadata Storage** - Stores system information with each backup

## Requirements

- Fedora Linux (tested on Fedora 43+)
- KDE Plasma 6.5 or higher
- Python 3.9+
- Qt6
- PyQt6

## Installation

### Quick Install from GitHub

```bash
# Clone the repository
git clone https://github.com/alduccino/KDE-Plasma-Backup-Manager.git
cd KDE-Plasma-Backup-Manager

# Run the installation script
chmod +x install.sh
./install.sh
```

The installation script will:
1. Install required system packages (python3, python3-qt6, qt6-qtbase)
2. Install Python dependencies (PyQt6)
3. Make the scripts executable
4. Create a desktop entry for the application menu
5. Create a command-line shortcut (if ~/.local/bin exists)
6. Optionally create the default backup directory

### Alternative: Download Release

```bash
# Download the latest release
wget https://github.com/alduccino/KDE-Plasma-Backup-Manager/archive/refs/heads/main.zip
unzip main.zip
cd KDE-Plasma-Backup-Manager-main

# Run installer
chmod +x install.sh
./install.sh
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/alduccino/KDE-Plasma-Backup-Manager.git
cd KDE-Plasma-Backup-Manager

# Install system dependencies
sudo dnf install python3 python3-pip python3-qt6 qt6-qtbase

# Install Python dependencies
pip install --user -r requirements.txt

# Make executable
chmod +x plasma-backup-manager.py plasma-backup-cli.py plasma-backup-auto.sh

# Run
./plasma-backup-manager.py
```

## Setting Up NAS Storage

### Automatic NFS Mount (Recommended)

Create an NFS mount in `/etc/fstab`:

```bash
# Edit fstab
sudo nano /etc/fstab

# Add your NAS mount (example):
192.168.1.100:/volume1/Backups  /home/YOUR_USERNAME/NAS  nfs  defaults,user,rw,auto  0  0
```

Create the mount point and mount:

```bash
mkdir -p ~/NAS
sudo mount -a
```

### Manual Mount

```bash
# Create mount point
mkdir -p ~/NAS

# Mount NFS share (example)
sudo mount -t nfs 192.168.1.100:/volume1/Backups ~/NAS

# For CIFS/SMB shares
sudo mount -t cifs //192.168.1.100/Backups ~/NAS -o username=YOUR_USER,password=YOUR_PASS
```

### Verify Mount

```bash
df -h | grep NAS
ls ~/NAS
```

## Usage

### Starting the Application

**From Application Menu:**
- Open the application menu
- Search for "Plasma Backup Manager"
- Click to launch

**From Terminal:**
```bash
# If installed with script
plasma-backup-manager

# Or directly
./plasma-backup-manager.py
```

### Creating a Backup

1. Open the application
2. Go to the **Backup** tab
3. Verify the backup path (default: `~/NAS/PlasmaBackup/[hostname]`)
4. Select what to backup:
   - ✓ KDE Plasma Settings & Plasmoids
   - ✓ Application Configurations
   - ✓ Firefox Profiles
   - ✓ Thunderbird Profiles
   - ✓ User Directories
5. Click **Start Backup**
6. Wait for completion (may take several minutes depending on data size)

### Restoring a Backup

1. Go to the **Restore** tab
2. Click **List Available Backups** to see all backups
3. Double-click a backup from the list, or manually enter the backup path
4. Read the warning carefully
5. Click **Start Restore**
6. After completion, **log out and log back in** for all changes to take effect

⚠️ **Important:** Restore will overwrite your current settings. Make sure you have a current backup before restoring!

## Backup Structure

Backups are organized as follows:

```
~/NAS/PlasmaBackup/
└── hostname/
    ├── 20241211_143022/
    │   ├── backup_metadata.json
    │   ├── kde/
    │   │   ├── .config/
    │   │   └── .local/share/
    │   ├── configs/
    │   ├── firefox/
    │   ├── thunderbird/
    │   └── user_data/
    │       ├── Documents/
    │       ├── Pictures/
    │       └── Videos/
    └── 20241211_150000/
        └── ...
```

### Metadata File

Each backup includes a `backup_metadata.json` file with:
- Timestamp
- Hostname
- Username
- Backup configuration
- KDE Plasma version
- Fedora version

## Customizing Backup Location

### In the GUI

1. Go to the **Backup** tab
2. In the "Backup Location" section, modify the path
3. Click **Browse...** to select a different directory

### Custom NAS Mount Point

If your NAS is mounted elsewhere:

```bash
# Example: NAS mounted at /mnt/nas
# In the application, change the path to:
/mnt/nas/PlasmaBackup/hostname
```

### Environment-Specific Paths

For multiple computers with different NAS locations, you can:

1. **Use hostname-based paths:**
   ```
   ~/NAS/PlasmaBackup/desktop-pc
   ~/NAS/PlasmaBackup/laptop
   ```

2. **Use custom paths per machine:**
   - Desktop: `/mnt/storage/Backups/desktop-pc`
   - Laptop: `~/NAS/Backups/laptop`

## Troubleshooting

### NAS Mount Issues

**Problem:** Backup location not accessible
```bash
# Check if NAS is mounted
df -h | grep NAS
mount | grep NAS

# Try remounting
sudo umount ~/NAS
sudo mount -a
```

**Problem:** Permission denied
```bash
# Check permissions
ls -la ~/NAS

# Ensure your user has write access
# For NFS, check server export permissions
# For CIFS, check mount options (uid, gid)
```

### Backup Fails

**Problem:** Insufficient disk space
```bash
# Check available space on NAS
df -h ~/NAS

# Check backup size estimate
du -sh ~/.mozilla ~/.thunderbird ~/Documents ~/Pictures ~/Videos
```

**Problem:** Backup takes too long
- Consider excluding large directories
- Use compression (future feature)
- Check network speed to NAS

### Restore Issues

**Problem:** Plasma doesn't restart after restore
```bash
# Manually restart Plasma
kquitapp6 plasmashell && plasmashell &

# Or log out and log back in
```

**Problem:** Settings not applied
- Make sure you logged out and logged back in
- Check file permissions in restored directories
- Verify the backup completed successfully

### Application Won't Start

**Problem:** Missing Qt6 libraries
```bash
# Reinstall Qt6
sudo dnf install python3-qt6 qt6-qtbase

# Verify PyQt6
python3 -c "from PyQt6 import QtWidgets; print('PyQt6 OK')"
```

**Problem:** Import errors
```bash
# Reinstall Python dependencies
pip install --user --force-reinstall -r requirements.txt
```

## Advanced Usage

### Command-Line Options

Currently the application is GUI-only, but you can script backups using the Python modules directly.

### Scheduled Backups

Create a systemd timer for automatic backups:

```bash
# Create timer unit
mkdir -p ~/.config/systemd/user/

cat > ~/.config/systemd/user/plasma-backup.service << EOF
[Unit]
Description=KDE Plasma Backup

[Service]
Type=oneshot
ExecStart=/path/to/plasma-backup-manager.py --auto-backup
EOF

cat > ~/.config/systemd/user/plasma-backup.timer << EOF
[Unit]
Description=Weekly Plasma Backup

[Timer]
OnCalendar=weekly
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Enable timer
systemctl --user enable plasma-backup.timer
systemctl --user start plasma-backup.timer
```

### Excluding Directories

To exclude specific directories, edit the script and modify the `backup_user_directories` method.

## Localization Support

The application automatically detects XDG user directory names from `~/.config/user-dirs.dirs`, which handles all localized directory names:

- **French:** Documents, Images, Vidéos, Musique, Téléchargements
- **German:** Dokumente, Bilder, Videos, Musik, Downloads
- **Spanish:** Documentos, Imágenes, Vídeos, Música, Descargas
- And more...

## Security Considerations

⚠️ **Important Security Notes:**

1. **SSH Keys:** The backup includes `~/.ssh/config` but NOT private keys for security
2. **Passwords:** Application passwords are backed up (Firefox, Thunderbird master passwords)
3. **NAS Security:** Ensure your NAS has proper access controls
4. **Backup Encryption:** Consider encrypting your NAS mount or using encrypted storage

### Recommended Security Practices

- Use encrypted NFS (Kerberos) or encrypted CIFS mounts
- Set proper file permissions on backup directory (700)
- Regularly rotate backups and delete old ones
- Store critical backups off-site
- Test restore procedures regularly

## What's NOT Backed Up

- System-wide configurations (require root access)
- Installed applications (use package manager)
- Flatpak/Snap applications and data
- Virtual machines
- Docker containers
- Steam games (use separate steam backup tools)
- Private SSH keys (for security reasons)
- Passwords stored in system keyring (security)

## FAQ

**Q: Can I use this on other distributions?**
A: It's designed for Fedora but should work on any Linux distribution with KDE Plasma 6.5+ and Qt6. You may need to adjust package installation commands.

**Q: Will this work with KDE Plasma 5?**
A: The application uses Qt6 and is designed for Plasma 6. For Plasma 5, you would need to modify it to use PyQt5.

**Q: Can I backup to a local directory instead of NAS?**
A: Yes! Just specify any local path in the backup location field.

**Q: How much space do I need?**
A: Depends on your data. KDE settings are typically < 100MB. Firefox/Thunderbird profiles can be several GB. User directories depend on your content.

**Q: Can I backup multiple computers to the same NAS?**
A: Yes! Each computer creates its own subdirectory based on hostname.

**Q: What if I change my hostname?**
A: The application uses the current hostname. To restore from a different hostname, manually specify the backup path.

**Q: Can I exclude specific plasmoids?**
A: Currently no, but you can edit the script to exclude specific configuration files.

## Contributing

This project is open source and welcomes contributions!

**Repository:** https://github.com/alduccino/KDE-Plasma-Backup-Manager

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution

- Additional backup targets (Steam, Lutris, etc.)
- Compression support (tar.gz, zip)
- Incremental backup functionality
- GUI improvements and translations
- Testing on other distributions
- Bug fixes and documentation improvements

### Reporting Issues

Found a bug or have a feature request? Please open an issue on GitHub:
https://github.com/alduccino/KDE-Plasma-Backup-Manager/issues

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

**In Brief:**
- ✅ You can use this software freely
- ✅ You can modify and distribute it
- ✅ You must include the license and copyright notice
- ✅ Changes must be documented
- ✅ Modified versions must also be GPL-3.0

For more details, see: https://www.gnu.org/licenses/gpl-3.0.html

## Version History

**v1.0.0** (2024-12-11)
- Initial release
- Qt6 GUI with Breeze theme integration
- Full KDE Plasma 6.5+ support
- NAS backup integration
- Localized directory name support
- Complete Firefox and Thunderbird backup
- Metadata storage and backup listing

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## Project Files

- **README.md** - This file, comprehensive documentation
- **QUICKSTART.md** - Quick start guide for new users
- **CHANGELOG.md** - Version history and release notes
- **CONTRIBUTING.md** - Guide for contributors
- **LICENSE** - GPL-3.0 license
- **PROJECT_STRUCTURE.md** - Detailed project structure documentation
- **.github/** - GitHub templates (issues, PRs)
- **plasma-backup-manager.py** - Main GUI application
- **plasma-backup-cli.py** - Command-line version
- **plasma-backup-auto.sh** - Automation wrapper script
- **install.sh** - Installation script
- **requirements.txt** - Python dependencies
- **systemd-examples.txt** - Systemd automation examples

## Credits

Developed for the KDE Plasma community on Fedora Linux.

## Support

### Getting Help

- **Documentation:** Read the [full README](README.md) and [Quick Start Guide](QUICKSTART.md)
- **Issues:** Report bugs or request features on [GitHub Issues](https://github.com/alduccino/KDE-Plasma-Backup-Manager/issues)
- **Discussions:** Join the conversation on [GitHub Discussions](https://github.com/alduccino/KDE-Plasma-Backup-Manager/discussions)

### Before Reporting Issues

For issues and questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Verify your system meets the [Requirements](#requirements)
3. Test with a fresh backup on a non-critical system first
4. Search existing [GitHub Issues](https://github.com/alduccino/KDE-Plasma-Backup-Manager/issues) to see if it's already reported

### Community

This is a community-driven project for KDE Plasma users. We welcome:
- Bug reports
- Feature requests
- Code contributions
- Documentation improvements
- Translations
- Testing on different systems

---

**Happy Backing Up! 🎉**
