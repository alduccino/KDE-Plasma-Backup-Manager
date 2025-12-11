#!/usr/bin/env python3
"""
KDE Plasma Backup Manager - CLI Version
For automated/scheduled backups without GUI
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# Import the backup worker from the main script
sys.path.insert(0, os.path.dirname(__file__))

# We'll create a simplified version that doesn't require PyQt6
import shutil
import subprocess

def safe_copytree(src, dst, ignore_errors=True):
    """
    Safely copy directory tree, handling symlinks and permission errors.
    This is NAS-friendly and won't fail on problematic symlinks.
    Uses manual recursive copy to have full control over error handling.
    """
    src = Path(src)
    dst = Path(dst)
    
    try:
        dst.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        if not ignore_errors:
            raise
        return
    
    try:
        items = list(src.iterdir())
    except (OSError, PermissionError) as e:
        if not ignore_errors:
            raise
        return
    
    for item in items:
        dst_item = dst / item.name
        
        try:
            # Check if it's a symlink
            if item.is_symlink():
                # Try to resolve the symlink
                try:
                    real_path = item.resolve(strict=True)
                    
                    # If it points to a file, copy the file content
                    if real_path.is_file():
                        shutil.copyfile(str(real_path), str(dst_item))
                    # If it points to a directory, skip it to avoid loops and issues
                    # Directory symlinks on NAS often cause permission errors
                    elif real_path.is_dir():
                        # Skip directory symlinks
                        continue
                except (OSError, PermissionError, RuntimeError):
                    # Broken symlink or permission error - skip it
                    continue
                    
            elif item.is_file():
                # Regular file - copy it
                try:
                    shutil.copyfile(str(item), str(dst_item))
                except (OSError, PermissionError) as e:
                    if not ignore_errors:
                        raise
                    # Skip files that can't be copied
                    continue
                    
            elif item.is_dir():
                # Regular directory - recurse into it
                safe_copytree(str(item), str(dst_item), ignore_errors=ignore_errors)
                
        except (OSError, PermissionError) as e:
            if not ignore_errors:
                raise
            # Skip items that cause errors
            continue

class BackupManagerCLI:
    def __init__(self):
        self.home = str(Path.home())
        self.hostname = os.uname().nodename
        self.default_backup_base = str(Path.home() / "NAS" / "Backups" / "Fedora" / "KDE")
        
        # Try to load custom backup path from config
        self.load_backup_config()
        
        self.backup_path = str(Path(self.default_backup_base) / self.hostname)
    
    def load_backup_config(self):
        """Load custom backup path from config file if it exists"""
        config_file = Path.home() / ".config" / "plasma-backup-manager" / "config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    if 'backup_base_path' in config:
                        self.default_backup_base = config['backup_base_path']
            except:
                pass  # Use default if config can't be read
    
    def log(self, message):
        """Print log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def backup(self, config=None, backup_path=None):
        """Perform backup"""
        if backup_path is None:
            backup_path = self.backup_path
        
        if config is None:
            config = {
                'kde_settings': True,
                'app_configs': True,
                'firefox': True,
                'thunderbird': True,
                'user_dirs': True,
            }
        
        try:
            # Create backup directory structure
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = Path(backup_path) / timestamp
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            self.log(f"Creating backup in: {backup_dir}")
            
            # Backup components
            if config['kde_settings']:
                self.backup_kde_settings(backup_dir)
            
            if config['app_configs']:
                self.backup_app_configs(backup_dir)
            
            if config['firefox']:
                self.backup_firefox(backup_dir)
            
            if config['thunderbird']:
                self.backup_thunderbird(backup_dir)
            
            if config['user_dirs']:
                self.backup_user_directories(backup_dir)
            
            # Save metadata
            self.save_metadata(backup_dir, timestamp, config)
            
            self.log(f"✓ Backup completed successfully: {backup_dir}")
            return True, str(backup_dir)
            
        except Exception as e:
            self.log(f"✗ Backup failed: {str(e)}")
            return False, str(e)
    
    def backup_kde_settings(self, backup_dir):
        """Backup KDE Plasma settings"""
        self.log("Backing up KDE Plasma settings...")
        
        kde_dir = backup_dir / "kde"
        kde_dir.mkdir(exist_ok=True)
        
        config_paths = [
            ".config/plasma*",
            ".config/kde*",
            ".config/kwin*",
            ".config/kglobalshortcutsrc",
            ".config/khotkeysrc",
            ".config/kdeglobals",
            ".config/kscreenlockerrc",
            ".config/systemsettingsrc",
            ".local/share/plasma",
            ".local/share/kwin",
            ".local/share/konsole",
            ".local/share/color-schemes",
            ".local/share/kxmlgui5",
            ".local/share/applications",
        ]
        
        for pattern in config_paths:
            self.copy_pattern(self.home, kde_dir, pattern)
        
        self.log("  ✓ KDE settings backed up")
    
    def backup_app_configs(self, backup_dir):
        """Backup application configurations"""
        self.log("Backing up application configurations...")
        
        config_dir = backup_dir / "configs"
        config_dir.mkdir(exist_ok=True)
        
        specific_apps = [
            ".config/Code",
            ".config/discord",
            ".config/Slack",
            ".vscode",
            ".bashrc",
            ".bash_profile",
            ".profile",
            ".zshrc",
            ".gitconfig",
            ".ssh/config",
        ]
        
        for app_path in specific_apps:
            src = Path(self.home) / app_path
            if src.exists():
                dst = config_dir / app_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.is_dir():
                    safe_copytree(str(src), str(dst), ignore_errors=True)
                else:
                    shutil.copyfile(src, dst)
        
        self.log("  ✓ Application configs backed up")
    
    def backup_firefox(self, backup_dir):
        """Backup Firefox profiles"""
        self.log("Backing up Firefox profiles...")
        
        firefox_src = Path(self.home) / ".mozilla/firefox"
        if firefox_src.exists():
            firefox_dst = backup_dir / "firefox"
            safe_copytree(str(firefox_src), str(firefox_dst), ignore_errors=True)
            self.log("  ✓ Firefox profiles backed up")
        else:
            self.log("  ⊘ Firefox profiles not found, skipping")
    
    def backup_thunderbird(self, backup_dir):
        """Backup Thunderbird profiles"""
        self.log("Backing up Thunderbird profiles...")
        
        thunderbird_src = Path(self.home) / ".thunderbird"
        if thunderbird_src.exists():
            thunderbird_dst = backup_dir / "thunderbird"
            safe_copytree(str(thunderbird_src), str(thunderbird_dst), ignore_errors=True)
            self.log("  ✓ Thunderbird profiles backed up")
        else:
            self.log("  ⊘ Thunderbird profiles not found, skipping")
    
    def backup_user_directories(self, backup_dir):
        """Backup user directories"""
        self.log("Backing up user directories...")
        
        user_dirs = self.get_xdg_user_dirs()
        data_dir = backup_dir / "user_data"
        data_dir.mkdir(exist_ok=True)
        
        for dir_type, dir_path in user_dirs.items():
            if dir_path and Path(dir_path).exists():
                self.log(f"  Backing up {dir_type}...")
                dst = data_dir / dir_type
                try:
                    safe_copytree(str(dir_path), str(dst), ignore_errors=True)
                    self.log(f"  ✓ {dir_type} backed up")
                except Exception as e:
                    self.log(f"  ⚠ Could not backup {dir_type}: {str(e)}")
    
    def get_xdg_user_dirs(self):
        """Get XDG user directories"""
        dirs = {}
        config_file = Path(self.home) / ".config/user-dirs.dirs"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('XDG_') and '=' in line:
                        key, value = line.split('=', 1)
                        value = value.strip('"').replace('$HOME', self.home)
                        
                        if 'DOCUMENTS' in key:
                            dirs['Documents'] = value
                        elif 'PICTURES' in key:
                            dirs['Pictures'] = value
                        elif 'VIDEOS' in key:
                            dirs['Videos'] = value
                        elif 'MUSIC' in key:
                            dirs['Music'] = value
                        elif 'DOWNLOAD' in key:
                            dirs['Downloads'] = value
        else:
            dirs = {
                'Documents': os.path.join(self.home, 'Documents'),
                'Pictures': os.path.join(self.home, 'Pictures'),
                'Videos': os.path.join(self.home, 'Videos'),
                'Music': os.path.join(self.home, 'Music'),
                'Downloads': os.path.join(self.home, 'Downloads'),
            }
        
        return dirs
    
    def copy_pattern(self, src_base, dst_base, pattern):
        """Copy files matching a pattern"""
        src_path = Path(src_base)
        
        if '*' in pattern:
            parts = pattern.split('/')
            current = src_path
            
            for part in parts[:-1]:
                current = current / part
            
            if current.exists():
                for item in current.glob(parts[-1]):
                    rel_path = item.relative_to(src_path)
                    dst = Path(dst_base) / rel_path
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    
                    if item.is_dir():
                        safe_copytree(str(item), str(dst), ignore_errors=True)
                    else:
                        shutil.copyfile(item, dst)
        else:
            src = src_path / pattern
            if src.exists():
                dst = Path(dst_base) / pattern
                dst.parent.mkdir(parents=True, exist_ok=True)
                
                if src.is_dir():
                    safe_copytree(str(src), str(dst), ignore_errors=True)
                else:
                    shutil.copyfile(src, dst)
    
    def save_metadata(self, backup_dir, timestamp, config):
        """Save backup metadata"""
        metadata = {
            'timestamp': timestamp,
            'hostname': self.hostname,
            'user': os.getenv('USER'),
            'config': config,
            'kde_version': self.get_kde_version(),
            'fedora_version': self.get_fedora_version(),
        }
        
        metadata_file = backup_dir / "backup_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def get_kde_version(self):
        """Get KDE Plasma version"""
        try:
            result = subprocess.run(['plasmashell', '--version'], 
                                  capture_output=True, text=True)
            return result.stdout.strip()
        except:
            return "Unknown"
    
    def get_fedora_version(self):
        """Get Fedora version"""
        try:
            with open('/etc/fedora-release', 'r') as f:
                return f.read().strip()
        except:
            return "Unknown"
    
    def list_backups(self, backup_base=None):
        """List available backups"""
        if backup_base is None:
            backup_base = self.backup_path
        
        base_path = Path(backup_base)
        
        if not base_path.exists():
            self.log(f"Backup location does not exist: {base_path}")
            return []
        
        backups = []
        for item in base_path.iterdir():
            if item.is_dir():
                metadata_file = item / "backup_metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        
                        backups.append({
                            'path': str(item),
                            'timestamp': metadata.get('timestamp', item.name),
                            'hostname': metadata.get('hostname', 'Unknown'),
                            'kde_version': metadata.get('kde_version', 'Unknown'),
                        })
                    except:
                        backups.append({
                            'path': str(item),
                            'timestamp': item.name,
                            'hostname': 'Unknown',
                            'kde_version': 'Unknown',
                        })
        
        backups.sort(key=lambda x: x['timestamp'], reverse=True)
        return backups


def main():
    parser = argparse.ArgumentParser(
        description='KDE Plasma Backup Manager - CLI Version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a full backup
  %(prog)s backup
  
  # Create backup with custom path
  %(prog)s backup --path /mnt/external/backups
  
  # Backup only KDE settings
  %(prog)s backup --kde-only
  
  # List available backups
  %(prog)s list
  
  # Show system info
  %(prog)s info
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create a backup')
    backup_parser.add_argument('--path', help='Custom backup path')
    backup_parser.add_argument('--kde-only', action='store_true', 
                              help='Backup only KDE settings')
    backup_parser.add_argument('--no-firefox', action='store_true',
                              help='Skip Firefox backup')
    backup_parser.add_argument('--no-thunderbird', action='store_true',
                              help='Skip Thunderbird backup')
    backup_parser.add_argument('--no-user-dirs', action='store_true',
                              help='Skip user directories backup')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available backups')
    list_parser.add_argument('--path', help='Custom backup base path')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show system information')
    
    args = parser.parse_args()
    
    manager = BackupManagerCLI()
    
    if args.command == 'backup':
        config = {
            'kde_settings': True,
            'app_configs': not args.kde_only,
            'firefox': not args.kde_only and not args.no_firefox,
            'thunderbird': not args.kde_only and not args.no_thunderbird,
            'user_dirs': not args.kde_only and not args.no_user_dirs,
        }
        
        success, result = manager.backup(config, args.path)
        sys.exit(0 if success else 1)
    
    elif args.command == 'list':
        backups = manager.list_backups(args.path)
        
        if not backups:
            manager.log("No backups found")
        else:
            manager.log(f"Found {len(backups)} backup(s):")
            for backup in backups:
                print(f"\n  Timestamp: {backup['timestamp']}")
                print(f"  Hostname:  {backup['hostname']}")
                print(f"  KDE:       {backup['kde_version']}")
                print(f"  Path:      {backup['path']}")
    
    elif args.command == 'info':
        print(f"Hostname:       {manager.hostname}")
        print(f"User:           {os.getenv('USER')}")
        print(f"Home:           {manager.home}")
        print(f"KDE Version:    {manager.get_kde_version()}")
        print(f"OS:             {manager.get_fedora_version()}")
        print(f"Default Backup: {manager.backup_path}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
