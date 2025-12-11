#!/bin/bash
# Installation script for KDE Plasma Backup Manager

set -e

echo "=========================================="
echo "KDE Plasma Backup Manager - Installation"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running on Fedora
if [ ! -f /etc/fedora-release ]; then
    echo -e "${YELLOW}Warning: This script is designed for Fedora Linux${NC}"
    echo "It may work on other distributions but is untested."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${BLUE}Installing system dependencies...${NC}"

# Install Python and Qt dependencies
sudo dnf install -y python3 python3-pip python3-qt6 qt6-qtbase

echo -e "${GREEN}✓ System dependencies installed${NC}"
echo ""

echo -e "${BLUE}Installing Python dependencies...${NC}"

# Install Python packages
pip install --user -r requirements.txt

echo -e "${GREEN}✓ Python dependencies installed${NC}"
echo ""

# Make the script executable
chmod +x plasma-backup-manager.py

# Create desktop entry
DESKTOP_FILE="$HOME/.local/share/applications/plasma-backup-manager.desktop"
mkdir -p "$HOME/.local/share/applications"

echo -e "${BLUE}Creating desktop entry...${NC}"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Plasma Backup Manager
Comment=Backup and restore KDE Plasma settings and user data
Exec=$(pwd)/plasma-backup-manager.py
Icon=system-software-update
Terminal=false
Categories=System;Utility;Qt;KDE;
Keywords=backup;restore;plasma;kde;settings;
EOF

echo -e "${GREEN}✓ Desktop entry created${NC}"
echo ""

# Create symlink in user bin if it exists
if [ -d "$HOME/.local/bin" ]; then
    ln -sf "$(pwd)/plasma-backup-manager.py" "$HOME/.local/bin/plasma-backup-manager"
    echo -e "${GREEN}✓ Command-line shortcut created: plasma-backup-manager${NC}"
    echo ""
fi

# Create default backup directory structure
DEFAULT_BACKUP_DIR="$HOME/NAS/PlasmaBackup"
echo -e "${BLUE}Setting up default backup directory...${NC}"
echo "Default location: $DEFAULT_BACKUP_DIR"
echo ""
echo "Note: This assumes your NAS is mounted at ~/NAS/"
echo "If your NAS is mounted elsewhere, you can change this in the application."
echo ""

read -p "Create default backup directory? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p "$DEFAULT_BACKUP_DIR"
    echo -e "${GREEN}✓ Default backup directory created${NC}"
fi

echo ""
echo -e "${GREEN}=========================================="
echo "Installation Complete!"
echo "==========================================${NC}"
echo ""
echo "You can now run the application by:"
echo "  1. Finding 'Plasma Backup Manager' in your application menu"
echo "  2. Running: ./plasma-backup-manager.py"
if [ -d "$HOME/.local/bin" ]; then
    echo "  3. Running: plasma-backup-manager (from terminal)"
fi
echo ""
echo -e "${YELLOW}Important Notes:${NC}"
echo "• Make sure your NAS is properly mounted before creating backups"
echo "• The default backup location is ~/NAS/PlasmaBackup/[hostname]"
echo "• You can customize the backup location in the application"
echo "• Always test restore on a non-critical system first"
echo ""
echo -e "${BLUE}For NAS mounting help, see the README.md file${NC}"
echo ""
