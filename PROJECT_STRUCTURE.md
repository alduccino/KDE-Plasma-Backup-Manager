# KDE Plasma Backup Manager - Project Structure

## File Overview

### Main Application
- **plasma-backup-manager.py** - Main Qt6 GUI application with full backup/restore functionality
- **plasma-backup-cli.py** - Command-line version for scripting and automation
- **plasma-backup-auto.sh** - Shell wrapper for automated backups (cron/systemd)

### Installation & Setup
- **install.sh** - Installation script for dependencies and desktop integration
- **requirements.txt** - Python package dependencies

### Documentation
- **README.md** - Comprehensive documentation with all features and troubleshooting
- **QUICKSTART.md** - Quick start guide for new users
- **systemd-examples.txt** - Example systemd service/timer for scheduled backups

## Directory Structure After Installation

```
plasma-backup-manager/
├── plasma-backup-manager.py    # Main GUI application
├── plasma-backup-cli.py         # CLI version
├── plasma-backup-auto.sh        # Automation wrapper
├── install.sh                   # Installer
├── requirements.txt             # Dependencies
├── README.md                    # Full documentation
├── QUICKSTART.md                # Quick guide
└── systemd-examples.txt         # Systemd examples

After installation:
~/.local/share/applications/
└── plasma-backup-manager.desktop   # Desktop entry

~/.local/bin/
└── plasma-backup-manager           # Symlink to main script

~/NAS/PlasmaBackup/                 # Default backup location
└── hostname/
    └── 20241211_143022/            # Timestamped backup
        ├── backup_metadata.json
        ├── kde/
        ├── configs/
        ├── firefox/
        ├── thunderbird/
        └── user_data/
```

## Backup Structure Details

### backup_metadata.json
Contains:
- Timestamp
- Hostname
- Username
- Backup configuration (what was backed up)
- KDE Plasma version
- Fedora version

### kde/
Contains all KDE Plasma configurations:
- .config/plasma* (Plasma settings)
- .config/kde* (KDE global settings)
- .config/kwin* (Window manager settings)
- .config/kglobalshortcutsrc (Keyboard shortcuts)
- .local/share/plasma (Plasmoid data)
- .local/share/konsole (Terminal profiles)
- .local/share/color-schemes (Color themes)

### configs/
Contains application configurations:
- .config/Code (VS Code)
- .vscode (VS Code settings)
- .bashrc, .zshrc (Shell configs)
- .gitconfig (Git settings)
- .ssh/config (SSH config)
- Other application configs

### firefox/
Complete Firefox profile backup:
- All profiles from ~/.mozilla/firefox
- Bookmarks, extensions, passwords
- Browser settings and history

### thunderbird/
Complete Thunderbird profile backup:
- All profiles from ~/.thunderbird
- Email accounts, messages
- Filters, settings, contacts

### user_data/
User directories with localization support:
- Documents (or "Documents" in French)
- Pictures (or "Images" in French)
- Videos (or "Vidéos" in French)
- Music (or "Musique" in French)
- Downloads (or "Téléchargements" in French)

## Usage Patterns

### GUI Usage
```bash
# Launch from application menu
# Or from terminal:
plasma-backup-manager
./plasma-backup-manager.py
```

### CLI Usage
```bash
# Full backup
./plasma-backup-cli.py backup

# Custom path
./plasma-backup-cli.py backup --path /mnt/backup

# KDE settings only
./plasma-backup-cli.py backup --kde-only

# List backups
./plasma-backup-cli.py list

# System info
./plasma-backup-cli.py info
```

### Automated Backups
```bash
# Using the wrapper script
./plasma-backup-auto.sh

# With cron (weekly)
0 2 * * 0 /path/to/plasma-backup-auto.sh

# With systemd (see systemd-examples.txt)
systemctl --user enable plasma-backup.timer
systemctl --user start plasma-backup.timer
```

## Configuration Options

### Environment Variables (for automation)
- `BACKUP_PATH` - Override default backup location
- `CLEANUP_OLD_BACKUPS=true` - Enable automatic cleanup (keep 5 most recent)
- `SEND_NOTIFICATIONS=true` - Enable desktop notifications

### GUI Configuration
- Backup location (browse or type path)
- Select components to backup (checkboxes)
- List and browse available backups

### CLI Configuration
- `--path` - Custom backup path
- `--kde-only` - Backup only KDE settings
- `--no-firefox` - Skip Firefox backup
- `--no-thunderbird` - Skip Thunderbird backup
- `--no-user-dirs` - Skip user directories

## File Permissions

Recommended permissions:
```bash
# Scripts
chmod 755 plasma-backup-manager.py
chmod 755 plasma-backup-cli.py
chmod 755 plasma-backup-auto.sh
chmod 755 install.sh

# Backup directory
chmod 700 ~/NAS/PlasmaBackup

# Backups
chmod -R 700 ~/NAS/PlasmaBackup/hostname/
```

## Log Files

Automated backups log to:
```
~/.local/share/plasma-backup-manager/backup.log
```

Log format:
```
[2024-12-11 14:30:22] Starting automated KDE Plasma backup
[2024-12-11 14:30:22] NAS is mounted at /home/user/NAS
[2024-12-11 14:30:22] Backup location: /home/user/NAS/PlasmaBackup/hostname
[2024-12-11 14:30:22] Starting backup...
[2024-12-11 14:35:45] Backup completed successfully
```

## Dependencies

### System Packages (Fedora)
- python3
- python3-pip
- python3-qt6
- qt6-qtbase

### Python Packages
- PyQt6 >= 6.5.0

### Runtime Requirements
- KDE Plasma 6.5+
- Fedora Linux (or compatible)
- Mounted NAS (if using network storage)

## Integration Points

### Desktop Integration
- Application menu entry
- System Settings integration (future)
- KDE notifications

### Network Storage
- NFS mounts
- CIFS/SMB shares
- Local directories
- External drives

### Automation
- Cron jobs
- systemd timers
- Manual scripting

## Future Enhancements (Ideas)

- Compression support (tar.gz, zip)
- Incremental backups
- Encryption support
- Remote backup destinations (rsync, rclone)
- Backup verification/checksums
- Restore previews
- Selective file restore
- Backup comparison tool
- Backup size estimation
- Bandwidth throttling
- Email notifications
- Web interface

## Support & Troubleshooting

See README.md for comprehensive troubleshooting guide covering:
- NAS mount issues
- Permission problems
- Backup failures
- Restore issues
- Application errors
- Network problems

## Version Information

Current Version: 1.0.0
Release Date: 2024-12-11
Platform: Fedora Linux with KDE Plasma 6.5+
License: Personal/Educational Use

## Contact & Contribution

This is a community tool for KDE Plasma users.
Contributions and improvements are welcome!
