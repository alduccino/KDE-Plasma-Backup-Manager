# Changelog

All notable changes to KDE Plasma Backup Manager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Interactive backup location selection during installation
- Support for custom backup paths (NAS, external drives, secondary disks, local directories)
- Configuration file to save custom backup location
- Better symlink handling for NAS/CIFS compatibility

### Changed
- Default backup path changed from `~/NAS/PlasmaBackup` to `~/NAS/Backups/Fedora/KDE`
- Improved error handling for symlinks and permission issues
- Installation script now prompts for backup location preference

### Fixed
- Symlink copy errors on NFS/CIFS mounts
- Permission denied errors when backing up to network storage
- Broken symlinks causing backup failures

## [1.0.0] - 2024-12-11

### Added
- Initial release
- Qt6 GUI application with native KDE Plasma integration
- Complete KDE Plasma settings backup (including plasmoids)
- Firefox profile backup (complete with extensions, bookmarks, passwords)
- Thunderbird profile backup (complete with emails, accounts, filters)
- Application configurations backup (.bashrc, git, SSH, VS Code, etc.)
- User directories backup with localization support
- Automatic detection of XDG user directories (supports French, German, Spanish, etc.)
- NAS integration with default path `~/NAS/PlasmaBackup/[hostname]`
- Per-hostname backup organization
- Timestamped backup versions
- Metadata storage (system info, KDE version, Fedora version)
- One-click restore functionality
- Real-time progress tracking
- Backup browsing and listing
- CLI version for scripting and automation
- Shell wrapper for cron/systemd automation
- Systemd timer examples
- Desktop entry for application menu integration
- Comprehensive documentation (README, Quick Start, Project Structure)
- Installation script with dependency management

### Features
- **GUI Application**: Full Qt6 interface with Breeze theme
- **CLI Application**: Command-line interface for automation
- **Automation Support**: Shell wrapper and systemd examples
- **Localization**: Automatic detection of localized directory names
- **Safety Features**: Confirmation dialogs and warnings for destructive operations
- **Progress Tracking**: Real-time updates during backup and restore
- **Backup Metadata**: Stores system information with each backup
- **Multi-computer Support**: Organizes backups by hostname

### Compatibility
- Fedora Linux 43+
- KDE Plasma 6.5+
- Python 3.9+
- Qt 6
- PyQt6 6.5.0+

### Known Limitations
- Does not backup system-wide configurations (requires root)
- Does not backup Flatpak/Snap application data
- Does not backup Steam games (separate tools recommended)
- No compression support yet
- No incremental backup support yet
- No encryption support yet

## [0.9.0] - 2024-12-11 (Pre-release)

### Added
- Initial development version
- Basic backup functionality
- GUI prototype

---

## Release Notes

### Version 1.0.0

This is the first public release of KDE Plasma Backup Manager. It provides a comprehensive backup solution for KDE Plasma users on Fedora Linux.

**Highlights:**
- Complete backup of KDE Plasma settings, including all plasmoid configurations
- Full Firefox and Thunderbird profile backups
- Automatic detection of localized user directory names (Documents/Images/Vidéos)
- NAS integration for network storage backups
- Both GUI and CLI interfaces
- Easy one-click restore with safety warnings

**Important Notes:**
- Always test restore functionality on a non-critical system first
- Make sure your NAS is properly mounted before starting backups
- Log out and log back in after restore for changes to take full effect

**System Requirements:**
- Fedora Linux (or compatible RPM-based distribution)
- KDE Plasma 6.5 or higher
- Python 3.9 or higher
- Qt 6 and PyQt6

**Installation:**
```bash
git clone https://github.com/alduccino/KDE-Plasma-Backup-Manager.git
cd KDE-Plasma-Backup-Manager
./install.sh
```

**Feedback:**
We welcome your feedback! Please report issues or suggest features on our GitHub repository:
https://github.com/alduccino/KDE-Plasma-Backup-Manager/issues

---

[Unreleased]: https://github.com/alduccino/KDE-Plasma-Backup-Manager/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/alduccino/KDE-Plasma-Backup-Manager/releases/tag/v1.0.0
[0.9.0]: https://github.com/alduccino/KDE-Plasma-Backup-Manager/releases/tag/v0.9.0
