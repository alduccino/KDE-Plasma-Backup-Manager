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
# Note: python3-qt6 is not available in Fedora repos, we'll install PyQt6 via pip instead
sudo dnf install -y python3 python3-pip qt6-qtbase --skip-unavailable

echo -e "${GREEN}✓ System dependencies installed${NC}"
echo ""

echo -e "${BLUE}Installing Python dependencies...${NC}"

# Install Python packages (PyQt6 will be installed here)
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
Icon=$(pwd)/Plasma-backup.png
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
DEFAULT_BACKUP_DIR="$HOME/NAS/Backups/Fedora/KDE"
echo -e "${BLUE}Setting up backup location...${NC}"
echo ""
echo "The backup location is where all your backups will be stored."
echo "This can be:"
echo "  • A NAS mount point (e.g., ~/NAS/Backups/Fedora/KDE)"
echo "  • A secondary disk (e.g., /mnt/backup/KDE)"
echo "  • An external drive (e.g., /media/backup/KDE)"
echo "  • Any local directory"
echo ""
echo "Default location: $DEFAULT_BACKUP_DIR"
echo ""

read -p "Use default location? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    BACKUP_DIR="$DEFAULT_BACKUP_DIR"
else
    echo ""
    echo "Enter your preferred backup location:"
    echo "(Use absolute path, e.g., /mnt/backup/Fedora/KDE)"
    read -p "Path: " BACKUP_DIR
    
    # Expand ~ to home directory if present
    BACKUP_DIR="${BACKUP_DIR/#\~/$HOME}"
fi

echo ""
echo "Backup location will be: $BACKUP_DIR"
echo "Backups will be organized as: $BACKUP_DIR/[hostname]/[timestamp]/"
echo ""

read -p "Create this directory now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if mkdir -p "$BACKUP_DIR" 2>/dev/null; then
        echo -e "${GREEN}✓ Backup directory created: $BACKUP_DIR${NC}"
        
        # Save the custom path to a config file for the application to read
        CONFIG_DIR="$HOME/.config/plasma-backup-manager"
        mkdir -p "$CONFIG_DIR"
        cat > "$CONFIG_DIR/config.json" << EOF
{
    "backup_base_path": "$BACKUP_DIR"
}
EOF
        echo -e "${GREEN}✓ Backup location saved to configuration${NC}"
    else
        echo -e "${YELLOW}⚠ Could not create directory. You may need to create it manually or check permissions.${NC}"
        echo "The application will use: $BACKUP_DIR"
    fi
else
    echo -e "${YELLOW}⚠ Directory not created. Make sure it exists before running backups.${NC}"
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
echo "• Make sure your backup location is accessible before creating backups"
echo "• Your backups will be saved to: $BACKUP_DIR/[hostname]/"
echo "• You can change the backup location anytime in the application"
echo "• Each backup is timestamped for easy identification"
echo "• Always test restore on a non-critical system first"
echo ""
echo -e "${BLUE}For NAS mounting help, see the README.md file${NC}"
echo ""
