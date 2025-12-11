# Quick Start Guide - KDE Plasma Backup Manager

## Installation (5 minutes)

```bash
# 1. Clone the repository from GitHub
git clone https://github.com/alduccino/KDE-Plasma-Backup-Manager.git
cd KDE-Plasma-Backup-Manager

# 2. Run the installer (it will ask you to choose your backup location)
chmod +x install.sh
./install.sh

# 3. Follow the prompts:
#    - Choose default location (~/NAS/Backups/Fedora/KDE) or custom path
#    - Create the backup directory
#    - Done!

# 4. Launch from your application menu or terminal
```

## First Backup (2 minutes)

1. **Launch** the application from your menu
2. **Verify** the backup path shows: `~/NAS/Backups/Fedora/KDE/your-hostname` (or your custom path)
3. **Check** all the boxes (they're checked by default)
4. **Click** "Start Backup"
5. **Wait** for completion
6. **Done!** Your backup is saved

## Setting Up Storage (One-time, 5 minutes)

### Option 1: NAS Mount (Recommended for network storage)

```bash
# Create mount point
mkdir -p ~/NAS

# Add to /etc/fstab (replace with your NAS IP and path)
echo "192.168.1.100:/volume1/Backups  $HOME/NAS  nfs  defaults,user,rw,auto  0  0" | sudo tee -a /etc/fstab

# Mount it
sudo mount -a

# Verify
ls ~/NAS
```

### Option 2: External Drive

```bash
# Your drive is usually auto-mounted at:
/media/username/drive-name/

# During installation, use this path:
/media/username/drive-name/Backups/Fedora/KDE
```

### Option 3: Secondary Disk

```bash
# Mount your disk to a permanent location
sudo mkdir -p /mnt/storage
# Add mount entry to /etc/fstab, then:
sudo mount -a

# During installation, use:
/mnt/storage/Backups/Fedora/KDE
```

### Option 4: Local Directory

```bash
# Simply use any local directory:
/home/username/Backups/Fedora/KDE
# or
~/Backups/KDE
```

The installer will guide you through selecting and creating your preferred location.

## Restoring a Backup (2 minutes)

1. **Go to** the "Restore" tab
2. **Click** "List Available Backups"
3. **Double-click** the backup you want to restore
4. **Click** "Start Restore"
5. **Log out and log back in** when done
6. **Enjoy** your restored settings!

## Default Backup Path

```
~/NAS/Backups/Fedora/KDE/
└── your-hostname/
    └── 20241211_143022/  (timestamp)
        ├── kde/          (Plasma settings)
        ├── firefox/      (Firefox profiles)
        ├── thunderbird/  (Email)
        ├── configs/      (App configs)
        └── user_data/    (Documents, Pictures, etc.)
```

**Note:** You can choose a different path during installation:
- External drive: `/media/username/drive/Backups/Fedora/KDE/`
- Secondary disk: `/mnt/storage/Backups/Fedora/KDE/`
- Custom location: Any directory you prefer

## What Gets Backed Up?

✅ All KDE Plasma settings and widgets  
✅ All Firefox bookmarks, extensions, passwords  
✅ All Thunderbird emails and accounts  
✅ Application configurations  
✅ Documents, Pictures, Videos (with localized names)  

## Tips

- **First backup** may take 5-30 minutes depending on data size
- **Subsequent backups** create new timestamped folders
- **Multiple computers** can backup to the same NAS (organized by hostname)
- **French systems** automatically detect Images/Vidéos instead of Pictures/Videos
- **Test restore** on a backup before relying on it

## Common Issues

**"Backup location not found"**
- Your NAS isn't mounted. Run: `ls ~/NAS`
- Mount your NAS or change the backup path

**"Permission denied"**
- Check NAS permissions: `ls -la ~/NAS`
- Ensure you can write to the NAS

**"Application won't start"**
- Run: `sudo dnf install python3-qt6 qt6-qtbase`
- Then: `pip install --user -r requirements.txt`

## Need Help?

See the full README.md for detailed documentation and troubleshooting.

---

**That's it! You're ready to backup and restore your KDE Plasma system!** 🚀
