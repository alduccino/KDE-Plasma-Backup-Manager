#!/usr/bin/env python3
"""
KDE Plasma Backup Manager
A comprehensive backup and restore solution for KDE Plasma settings and user data
"""

import sys
import os
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QTextEdit, QTabWidget,
    QFileDialog, QMessageBox, QProgressBar, QLineEdit, QCheckBox,
    QGroupBox, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QFont

def safe_copytree(src, dst, ignore_errors=True, progress_callback=None):
    """
    Safely copy directory tree, handling symlinks and permission errors.
    This is NAS-friendly and won't fail on problematic symlinks.
    Uses manual recursive copy to have full control over error handling.
    Uses shutil.copyfile() to avoid ANY permission/metadata operations (NFS compatibility).
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
                        # Use copyfile() - only copies content, no permissions at all
                        shutil.copyfile(str(real_path), str(dst_item))
                    # If it points to a directory, skip it to avoid loops and issues
                    # Directory symlinks on NAS often cause permission errors
                    elif real_path.is_dir():
                        if progress_callback:
                            progress_callback(f"  ⊘ Skipped directory symlink: {item.name}")
                        continue
                except (OSError, PermissionError, RuntimeError):
                    # Broken symlink or permission error - skip it
                    if progress_callback:
                        progress_callback(f"  ⊘ Skipped broken symlink: {item.name}")
                    continue
                    
            elif item.is_file():
                # Regular file - copy content only, no permissions (NFS compatibility)
                try:
                    shutil.copyfile(str(item), str(dst_item))
                except (OSError, PermissionError) as e:
                    if not ignore_errors:
                        raise
                    if progress_callback:
                        progress_callback(f"  ⚠ Could not copy file: {item.name}")
                    continue
                    
            elif item.is_dir():
                # Regular directory - recurse into it
                safe_copytree(str(item), str(dst_item), ignore_errors=ignore_errors, progress_callback=progress_callback)
                
        except (OSError, PermissionError) as e:
            if not ignore_errors:
                raise
            if progress_callback:
                progress_callback(f"  ⚠ Error accessing: {item.name}")
            continue

class BackupWorker(QThread):
    """Worker thread for backup operations"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, config, backup_path):
        super().__init__()
        self.config = config
        self.backup_path = backup_path
        self.home = str(Path.home())
        
    def run(self):
        try:
            # Create backup directory structure
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = Path(self.backup_path) / timestamp
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            self.progress.emit(f"Creating backup in: {backup_dir}")
            self.progress.emit("")
            
            # Backup KDE Plasma settings
            if self.config['kde_settings']:
                self.backup_kde_settings(backup_dir)
                self.progress.emit("")
            
            # Backup application configs
            if self.config['app_configs']:
                self.backup_app_configs(backup_dir)
                self.progress.emit("")
            
            # Backup Firefox profiles
            if self.config['firefox']:
                self.backup_firefox(backup_dir)
                self.progress.emit("")
            
            # Backup Thunderbird profiles
            if self.config['thunderbird']:
                self.backup_thunderbird(backup_dir)
                self.progress.emit("")
            
            # Backup user directories
            if self.config['user_dirs']:
                self.backup_user_directories(backup_dir)
                self.progress.emit("")
            
            # Save backup metadata
            self.save_metadata(backup_dir, timestamp)
            
            # Generate summary
            self.progress.emit("=== Backup Summary ===")
            for subdir in backup_dir.iterdir():
                if subdir.is_dir():
                    file_count = sum(1 for _ in subdir.rglob('*') if _.is_file())
                    size = sum(f.stat().st_size for f in subdir.rglob('*') if f.is_file())
                    size_mb = size / (1024 * 1024)
                    self.progress.emit(f"  {subdir.name}: {file_count} files, {size_mb:.1f} MB")
            
            total_size = sum(f.stat().st_size for f in backup_dir.rglob('*') if f.is_file())
            total_mb = total_size / (1024 * 1024)
            self.progress.emit(f"  Total: {total_mb:.1f} MB")
            self.progress.emit("")
            
            self.finished.emit(True, f"Backup completed successfully!\n\nLocation: {backup_dir}\nSize: {total_mb:.1f} MB")
            
        except Exception as e:
            import traceback
            error_msg = f"Backup failed: {str(e)}\n\nDetails:\n{traceback.format_exc()}"
            self.finished.emit(False, error_msg)
    
    def backup_kde_settings(self, backup_dir):
        """Backup KDE Plasma settings including plasmoids"""
        self.progress.emit("Backing up KDE Plasma settings...")
        
        kde_dir = backup_dir / "kde"
        kde_dir.mkdir(exist_ok=True)
        
        # KDE configuration files
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
        
        self.progress.emit("KDE settings backed up")
    
    def backup_app_configs(self, backup_dir):
        """Backup various application configurations"""
        self.progress.emit("Backing up application configurations...")
        
        config_dir = backup_dir / "configs"
        config_dir.mkdir(exist_ok=True)
        
        # Specific applications to backup
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
        
        backed_up_count = 0
        for app_path in specific_apps:
            src = Path(self.home) / app_path
            if src.exists():
                dst = config_dir / app_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                try:
                    if src.is_dir():
                        safe_copytree(str(src), str(dst), ignore_errors=True, progress_callback=self.progress.emit)
                        self.progress.emit(f"  ✓ Backed up {app_path}")
                        backed_up_count += 1
                    else:
                        shutil.copyfile(src, dst)
                        self.progress.emit(f"  ✓ Backed up {app_path}")
                        backed_up_count += 1
                except Exception as e:
                    self.progress.emit(f"  ⚠ Skipped {app_path}: {str(e)}")
        
        if backed_up_count > 0:
            self.progress.emit(f"Application configs backed up ({backed_up_count} items)")
        else:
            self.progress.emit("No application configs found to backup")
    
    def backup_firefox(self, backup_dir):
        """Backup Firefox profiles"""
        self.progress.emit("Backing up Firefox profiles...")
        
        firefox_src = Path(self.home) / ".mozilla/firefox"
        if firefox_src.exists():
            firefox_dst = backup_dir / "firefox"
            try:
                safe_copytree(str(firefox_src), str(firefox_dst), ignore_errors=True, progress_callback=self.progress.emit)
                self.progress.emit("Firefox profiles backed up")
            except Exception as e:
                self.progress.emit(f"Warning: Firefox backup had issues: {str(e)}")
        else:
            self.progress.emit("Firefox profiles not found, skipping")
    
    def backup_thunderbird(self, backup_dir):
        """Backup Thunderbird profiles"""
        self.progress.emit("Backing up Thunderbird profiles...")
        
        thunderbird_src = Path(self.home) / ".thunderbird"
        if thunderbird_src.exists():
            thunderbird_dst = backup_dir / "thunderbird"
            try:
                safe_copytree(str(thunderbird_src), str(thunderbird_dst), ignore_errors=True, progress_callback=self.progress.emit)
                self.progress.emit("Thunderbird profiles backed up")
            except Exception as e:
                self.progress.emit(f"Warning: Thunderbird backup had issues: {str(e)}")
        else:
            self.progress.emit("Thunderbird profiles not found, skipping")
    
    def backup_user_directories(self, backup_dir):
        """Backup user directories (Documents, Pictures, Videos)"""
        self.progress.emit("Backing up user directories...")
        
        # Get XDG user directories
        user_dirs = self.get_xdg_user_dirs()
        
        data_dir = backup_dir / "user_data"
        data_dir.mkdir(exist_ok=True)
        
        for dir_type, dir_path in user_dirs.items():
            if dir_path and Path(dir_path).exists():
                self.progress.emit(f"Backing up {dir_type}...")
                dst = data_dir / dir_type
                try:
                    safe_copytree(str(dir_path), str(dst), ignore_errors=True, progress_callback=self.progress.emit)
                    self.progress.emit(f"{dir_type} backed up")
                except Exception as e:
                    self.progress.emit(f"Warning: Could not backup {dir_type}: {str(e)}")
    
    def get_xdg_user_dirs(self):
        """Get XDG user directories (handles localized names)"""
        dirs = {}
        
        # Try to read from xdg-user-dirs
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
            # Fallback to default names
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
        
        # Handle wildcards
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
                    
                    try:
                        if item.is_dir():
                            safe_copytree(str(item), str(dst), ignore_errors=True, progress_callback=self.progress.emit)
                        else:
                            shutil.copyfile(item, dst)
                    except Exception as e:
                        self.progress.emit(f"  ⚠ Skipped {item.name}: {str(e)}")
        else:
            src = src_path / pattern
            if src.exists():
                dst = Path(dst_base) / pattern
                dst.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    if src.is_dir():
                        safe_copytree(str(src), str(dst), ignore_errors=True, progress_callback=self.progress.emit)
                    else:
                        shutil.copyfile(src, dst)
                except Exception as e:
                    self.progress.emit(f"  ⚠ Skipped {pattern}: {str(e)}")
    
    def save_metadata(self, backup_dir, timestamp):
        """Save backup metadata"""
        metadata = {
            'timestamp': timestamp,
            'hostname': os.uname().nodename,
            'user': os.getenv('USER'),
            'config': self.config,
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


class RestoreWorker(QThread):
    """Worker thread for restore operations"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, backup_path):
        super().__init__()
        self.backup_path = backup_path
        self.home = str(Path.home())
        
    def run(self):
        try:
            backup_dir = Path(self.backup_path)
            
            self.progress.emit(f"Restoring from: {backup_dir}")
            
            # Load metadata
            metadata = self.load_metadata(backup_dir)
            if metadata:
                self.progress.emit(f"Backup from: {metadata.get('timestamp', 'Unknown')}")
                self.progress.emit(f"Hostname: {metadata.get('hostname', 'Unknown')}")
            
            # Restore KDE settings
            kde_dir = backup_dir / "kde"
            if kde_dir.exists():
                self.restore_kde_settings(kde_dir)
            
            # Restore configs
            config_dir = backup_dir / "configs"
            if config_dir.exists():
                self.restore_configs(config_dir)
            
            # Restore Firefox
            firefox_dir = backup_dir / "firefox"
            if firefox_dir.exists():
                self.restore_firefox(firefox_dir)
            
            # Restore Thunderbird
            thunderbird_dir = backup_dir / "thunderbird"
            if thunderbird_dir.exists():
                self.restore_thunderbird(thunderbird_dir)
            
            # Restore user data
            data_dir = backup_dir / "user_data"
            if data_dir.exists():
                self.restore_user_data(data_dir)
            
            self.progress.emit("\n*** Restore completed! ***")
            self.progress.emit("Please log out and log back in for all changes to take effect.")
            self.finished.emit(True, "Restore completed successfully!")
            
        except Exception as e:
            self.finished.emit(False, f"Restore failed: {str(e)}")
    
    def load_metadata(self, backup_dir):
        """Load backup metadata"""
        metadata_file = backup_dir / "backup_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                return json.load(f)
        return None
    
    def restore_kde_settings(self, kde_dir):
        """Restore KDE settings"""
        self.progress.emit("Restoring KDE Plasma settings...")
        
        # Copy all KDE files back
        for item in kde_dir.rglob('*'):
            if item.is_file():
                rel_path = item.relative_to(kde_dir)
                dst = Path(self.home) / rel_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(item, dst)
        
        # Restart Plasma
        self.progress.emit("Restarting Plasma shell...")
        try:
            subprocess.run(['kquitapp6', 'plasmashell'], check=False)
            QTimer.singleShot(2000, lambda: subprocess.Popen(['plasmashell']))
        except:
            self.progress.emit("Note: Could not automatically restart Plasma")
    
    def restore_configs(self, config_dir):
        """Restore application configs"""
        self.progress.emit("Restoring application configurations...")
        
        for item in config_dir.rglob('*'):
            if item.is_file():
                rel_path = item.relative_to(config_dir)
                dst = Path(self.home) / rel_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(item, dst)
    
    def restore_firefox(self, firefox_dir):
        """Restore Firefox profiles"""
        self.progress.emit("Restoring Firefox profiles...")
        
        dst = Path(self.home) / ".mozilla/firefox"
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(firefox_dir, dst, symlinks=True)
    
    def restore_thunderbird(self, thunderbird_dir):
        """Restore Thunderbird profiles"""
        self.progress.emit("Restoring Thunderbird profiles...")
        
        dst = Path(self.home) / ".thunderbird"
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(thunderbird_dir, dst, symlinks=True)
    
    def restore_user_data(self, data_dir):
        """Restore user directories"""
        self.progress.emit("Restoring user directories...")
        
        # Get current XDG directories
        user_dirs = self.get_xdg_user_dirs()
        
        for dir_type in data_dir.iterdir():
            if dir_type.is_dir():
                dir_name = dir_type.name
                
                # Determine destination
                if dir_name in user_dirs:
                    dst = Path(user_dirs[dir_name])
                else:
                    dst = Path(self.home) / dir_name
                
                self.progress.emit(f"Restoring {dir_name} to {dst}...")
                dst.parent.mkdir(parents=True, exist_ok=True)
                
                # Merge directories
                for item in dir_type.rglob('*'):
                    if item.is_file():
                        rel_path = item.relative_to(dir_type)
                        dst_file = dst / rel_path
                        dst_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copyfile(item, dst_file)
    
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
        
        return dirs


class BackupManagerGUI(QMainWindow):
    """Main GUI window for backup manager"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KDE Plasma Backup Manager")
        self.setMinimumSize(900, 700)
        
        # Default settings
        self.hostname = os.uname().nodename
        self.default_backup_base = str(Path.home() / "NAS" / "Backups" / "Fedora" / "KDE")
        
        # Try to load custom backup path from config
        self.load_backup_config()
        
        self.backup_path = str(Path(self.default_backup_base) / self.hostname)
        
        self.init_ui()
    
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
        
    def init_ui(self):
        """Initialize the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("KDE Plasma Backup & Restore Manager")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Tab widget
        tabs = QTabWidget()
        
        # Backup tab
        backup_tab = self.create_backup_tab()
        tabs.addTab(backup_tab, "Backup")
        
        # Restore tab
        restore_tab = self.create_restore_tab()
        tabs.addTab(restore_tab, "Restore")
        
        # Settings tab
        settings_tab = self.create_settings_tab()
        tabs.addTab(settings_tab, "Settings")
        
        main_layout.addWidget(tabs)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
    def create_backup_tab(self):
        """Create the backup tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Backup location
        location_group = QGroupBox("Backup Location")
        location_layout = QVBoxLayout()
        
        path_layout = QHBoxLayout()
        self.backup_path_edit = QLineEdit(self.backup_path)
        path_layout.addWidget(QLabel("Path:"))
        path_layout.addWidget(self.backup_path_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_backup_location)
        path_layout.addWidget(browse_btn)
        
        location_layout.addLayout(path_layout)
        location_group.setLayout(location_layout)
        layout.addWidget(location_group)
        
        # What to backup
        options_group = QGroupBox("What to Backup")
        options_layout = QVBoxLayout()
        
        self.kde_settings_cb = QCheckBox("KDE Plasma Settings & Plasmoids")
        self.kde_settings_cb.setChecked(True)
        options_layout.addWidget(self.kde_settings_cb)
        
        self.app_configs_cb = QCheckBox("Application Configurations")
        self.app_configs_cb.setChecked(True)
        options_layout.addWidget(self.app_configs_cb)
        
        self.firefox_cb = QCheckBox("Firefox Profiles")
        self.firefox_cb.setChecked(True)
        options_layout.addWidget(self.firefox_cb)
        
        self.thunderbird_cb = QCheckBox("Thunderbird Profiles")
        self.thunderbird_cb.setChecked(True)
        options_layout.addWidget(self.thunderbird_cb)
        
        self.user_dirs_cb = QCheckBox("User Directories (Documents, Pictures, Videos, etc.)")
        self.user_dirs_cb.setChecked(True)
        options_layout.addWidget(self.user_dirs_cb)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Progress area
        self.backup_progress = QTextEdit()
        self.backup_progress.setReadOnly(True)
        self.backup_progress.setMaximumHeight(200)
        layout.addWidget(QLabel("Progress:"))
        layout.addWidget(self.backup_progress)
        
        # Backup button
        self.backup_btn = QPushButton("Start Backup")
        self.backup_btn.setMinimumHeight(40)
        self.backup_btn.clicked.connect(self.start_backup)
        layout.addWidget(self.backup_btn)
        
        layout.addStretch()
        
        return widget
    
    def create_restore_tab(self):
        """Create the restore tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Backup selection
        selection_group = QGroupBox("Select Backup to Restore")
        selection_layout = QVBoxLayout()
        
        path_layout = QHBoxLayout()
        self.restore_path_edit = QLineEdit()
        path_layout.addWidget(QLabel("Backup Path:"))
        path_layout.addWidget(self.restore_path_edit)
        
        browse_restore_btn = QPushButton("Browse...")
        browse_restore_btn.clicked.connect(self.browse_restore_location)
        path_layout.addWidget(browse_restore_btn)
        
        selection_layout.addLayout(path_layout)
        
        # List available backups
        list_btn = QPushButton("List Available Backups")
        list_btn.clicked.connect(self.list_backups)
        selection_layout.addWidget(list_btn)
        
        self.backup_list = QListWidget()
        self.backup_list.itemDoubleClicked.connect(self.select_backup_from_list)
        selection_layout.addWidget(self.backup_list)
        
        selection_group.setLayout(selection_layout)
        layout.addWidget(selection_group)
        
        # Progress area
        self.restore_progress = QTextEdit()
        self.restore_progress.setReadOnly(True)
        self.restore_progress.setMaximumHeight(200)
        layout.addWidget(QLabel("Progress:"))
        layout.addWidget(self.restore_progress)
        
        # Warning
        warning = QLabel("⚠ Warning: Restore will overwrite existing settings and data!")
        warning.setStyleSheet("color: red; font-weight: bold;")
        warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(warning)
        
        # Restore button
        self.restore_btn = QPushButton("Start Restore")
        self.restore_btn.setMinimumHeight(40)
        self.restore_btn.clicked.connect(self.start_restore)
        layout.addWidget(self.restore_btn)
        
        layout.addStretch()
        
        return widget
    
    def create_settings_tab(self):
        """Create the settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Info
        info_group = QGroupBox("System Information")
        info_layout = QVBoxLayout()
        
        info_layout.addWidget(QLabel(f"Hostname: {self.hostname}"))
        info_layout.addWidget(QLabel(f"User: {os.getenv('USER')}"))
        info_layout.addWidget(QLabel(f"Home: {Path.home()}"))
        
        try:
            result = subprocess.run(['plasmashell', '--version'], 
                                  capture_output=True, text=True)
            kde_version = result.stdout.strip()
        except:
            kde_version = "Unknown"
        info_layout.addWidget(QLabel(f"KDE: {kde_version}"))
        
        try:
            with open('/etc/fedora-release', 'r') as f:
                fedora_version = f.read().strip()
        except:
            fedora_version = "Unknown"
        info_layout.addWidget(QLabel(f"OS: {fedora_version}"))
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Default paths
        paths_group = QGroupBox("Default Paths")
        paths_layout = QVBoxLayout()
        
        paths_layout.addWidget(QLabel(f"Default backup location:"))
        default_path_label = QLabel(f"{self.default_backup_base}/[hostname]")
        default_path_label.setStyleSheet("font-family: monospace;")
        paths_layout.addWidget(default_path_label)
        
        paths_group.setLayout(paths_layout)
        layout.addWidget(paths_group)
        
        # About
        about_group = QGroupBox("About")
        about_layout = QVBoxLayout()
        
        about_text = QLabel(
            "KDE Plasma Backup Manager v1.0\n\n"
            "A comprehensive backup and restore solution for KDE Plasma settings,\n"
            "application configurations, and user data.\n\n"
            "Supports:\n"
            "• KDE Plasma settings and plasmoid configurations\n"
            "• Firefox and Thunderbird complete profiles\n"
            "• Application configurations\n"
            "• User directories (localized names supported)\n"
            "• Network storage (NAS) integration"
        )
        about_text.setWordWrap(True)
        about_layout.addWidget(about_text)
        
        about_group.setLayout(about_layout)
        layout.addWidget(about_group)
        
        layout.addStretch()
        
        return widget
    
    def browse_backup_location(self):
        """Browse for backup location"""
        path = QFileDialog.getExistingDirectory(
            self, "Select Backup Location", self.backup_path
        )
        if path:
            self.backup_path = path
            self.backup_path_edit.setText(path)
    
    def browse_restore_location(self):
        """Browse for restore location"""
        path = QFileDialog.getExistingDirectory(
            self, "Select Backup to Restore", self.backup_path
        )
        if path:
            self.restore_path_edit.setText(path)
    
    def list_backups(self):
        """List available backups"""
        self.backup_list.clear()
        
        base_path = Path(self.backup_path_edit.text() or self.backup_path)
        
        if not base_path.exists():
            QMessageBox.warning(
                self, "Path Not Found",
                f"Backup location does not exist:\n{base_path}"
            )
            return
        
        # Find backup directories
        backups = []
        for item in base_path.iterdir():
            if item.is_dir():
                metadata_file = item / "backup_metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        
                        timestamp = metadata.get('timestamp', item.name)
                        hostname = metadata.get('hostname', 'Unknown')
                        
                        backups.append({
                            'path': str(item),
                            'display': f"{timestamp} - {hostname}",
                            'timestamp': timestamp
                        })
                    except:
                        backups.append({
                            'path': str(item),
                            'display': item.name,
                            'timestamp': item.name
                        })
        
        # Sort by timestamp
        backups.sort(key=lambda x: x['timestamp'], reverse=True)
        
        for backup in backups:
            self.backup_list.addItem(f"{backup['display']}\n  → {backup['path']}")
    
    def select_backup_from_list(self, item):
        """Select a backup from the list"""
        text = item.text()
        # Extract path from the display text
        if '→' in text:
            path = text.split('→')[1].strip()
            self.restore_path_edit.setText(path)
    
    def start_backup(self):
        """Start backup process"""
        # Get configuration
        config = {
            'kde_settings': self.kde_settings_cb.isChecked(),
            'app_configs': self.app_configs_cb.isChecked(),
            'firefox': self.firefox_cb.isChecked(),
            'thunderbird': self.thunderbird_cb.isChecked(),
            'user_dirs': self.user_dirs_cb.isChecked(),
        }
        
        backup_path = self.backup_path_edit.text()
        
        if not backup_path:
            QMessageBox.warning(self, "No Path", "Please specify a backup location")
            return
        
        # Confirm
        reply = QMessageBox.question(
            self, "Confirm Backup",
            f"Start backup to:\n{backup_path}\n\nThis may take several minutes.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Clear progress
        self.backup_progress.clear()
        self.backup_btn.setEnabled(False)
        
        # Start worker thread
        self.backup_worker = BackupWorker(config, backup_path)
        self.backup_worker.progress.connect(self.update_backup_progress)
        self.backup_worker.finished.connect(self.backup_finished)
        self.backup_worker.start()
    
    def update_backup_progress(self, message):
        """Update backup progress display"""
        self.backup_progress.append(message)
        self.statusBar().showMessage(message)
    
    def backup_finished(self, success, message):
        """Handle backup completion"""
        self.backup_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "Backup Complete", message)
        else:
            QMessageBox.critical(self, "Backup Failed", message)
        
        self.statusBar().showMessage("Ready")
    
    def start_restore(self):
        """Start restore process"""
        restore_path = self.restore_path_edit.text()
        
        if not restore_path:
            QMessageBox.warning(self, "No Path", "Please select a backup to restore")
            return
        
        if not Path(restore_path).exists():
            QMessageBox.critical(self, "Path Not Found", 
                               f"Backup not found:\n{restore_path}")
            return
        
        # Strong warning
        reply = QMessageBox.warning(
            self, "Confirm Restore",
            "⚠ WARNING ⚠\n\n"
            "This will OVERWRITE your current settings and data!\n\n"
            f"Restoring from:\n{restore_path}\n\n"
            "Make sure you have a current backup before proceeding.\n\n"
            "Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Clear progress
        self.restore_progress.clear()
        self.restore_btn.setEnabled(False)
        
        # Start worker thread
        self.restore_worker = RestoreWorker(restore_path)
        self.restore_worker.progress.connect(self.update_restore_progress)
        self.restore_worker.finished.connect(self.restore_finished)
        self.restore_worker.start()
    
    def update_restore_progress(self, message):
        """Update restore progress display"""
        self.restore_progress.append(message)
        self.statusBar().showMessage(message)
    
    def restore_finished(self, success, message):
        """Handle restore completion"""
        self.restore_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(
                self, "Restore Complete",
                message + "\n\nPlease log out and log back in for all changes to take effect."
            )
        else:
            QMessageBox.critical(self, "Restore Failed", message)
        
        self.statusBar().showMessage("Ready")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("KDE Plasma Backup Manager")
    app.setStyle("Breeze")
    
    window = BackupManagerGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
