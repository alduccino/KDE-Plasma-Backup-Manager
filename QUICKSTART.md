# Quick Start Guide - KDE Plasma Backup Manager

## Installation (5 minutes)

```bash
# 1. Download or clone the files
cd plasma-backup-manager

# 2. Run the installer
chmod +x install.sh
./install.sh

# 3. Done! Launch from your application menu
```

## First Backup (2 minutes)

1. **Launch** the application from your menu
2. **Verify** the backup path shows: `~/NAS/PlasmaBackup/your-hostname`
3. **Check** all the boxes (they're checked by default)
4. **Click** "Start Backup"
5. **Wait** for completion
6. **Done!** Your backup is saved

## Setting Up NAS (One-time, 3 minutes)

### If you haven't mounted your NAS yet:

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

### If your NAS is already mounted elsewhere:

Just change the backup path in the application to point to your mount location.

## Restoring a Backup (2 minutes)

1. **Go to** the "Restore" tab
2. **Click** "List Available Backups"
3. **Double-click** the backup you want to restore
4. **Click** "Start Restore"
5. **Log out and log back in** when done
6. **Enjoy** your restored settings!

## Default Backup Path

```
~/NAS/PlasmaBackup/
└── your-hostname/
    └── 20241211_143022/  (timestamp)
        ├── kde/          (Plasma settings)
        ├── firefox/      (Firefox profiles)
        ├── thunderbird/  (Email)
        ├── configs/      (App configs)
        └── user_data/    (Documents, Pictures, etc.)
```

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
