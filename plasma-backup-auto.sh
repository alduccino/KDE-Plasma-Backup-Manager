#!/bin/bash
# Simple wrapper script for automated KDE Plasma backups
# Can be used with cron or systemd timers

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$HOME/.local/share/plasma-backup-manager/backup.log"
BACKUP_PATH="${BACKUP_PATH:-$HOME/NAS/PlasmaBackup/$(hostname)}"

# Create log directory
mkdir -p "$(dirname "$LOG_FILE")"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "========================================"
log "Starting automated KDE Plasma backup"
log "========================================"

# Check if NAS is mounted (if using NAS)
if [[ "$BACKUP_PATH" == *"/NAS/"* ]]; then
    NAS_MOUNT="$HOME/NAS"
    if ! mountpoint -q "$NAS_MOUNT" 2>/dev/null; then
        log "ERROR: NAS not mounted at $NAS_MOUNT"
        log "Attempting to mount..."
        
        # Try to mount
        if mount "$NAS_MOUNT" 2>/dev/null; then
            log "NAS mounted successfully"
        else
            log "ERROR: Failed to mount NAS"
            log "Backup aborted"
            exit 1
        fi
    else
        log "NAS is mounted at $NAS_MOUNT"
    fi
fi

# Check if backup directory is writable
if [ ! -w "$(dirname "$BACKUP_PATH")" ]; then
    log "ERROR: Backup directory not writable: $BACKUP_PATH"
    exit 1
fi

log "Backup location: $BACKUP_PATH"

# Run the CLI backup
log "Starting backup..."

if [ -f "$SCRIPT_DIR/plasma-backup-cli.py" ]; then
    python3 "$SCRIPT_DIR/plasma-backup-cli.py" backup --path "$BACKUP_PATH" >> "$LOG_FILE" 2>&1
    EXIT_CODE=$?
else
    log "ERROR: plasma-backup-cli.py not found in $SCRIPT_DIR"
    exit 1
fi

if [ $EXIT_CODE -eq 0 ]; then
    log "========================================"
    log "Backup completed successfully"
    log "========================================"
    
    # Optional: Clean up old backups (keep last 5)
    if [ "${CLEANUP_OLD_BACKUPS:-false}" = "true" ]; then
        log "Cleaning up old backups..."
        cd "$BACKUP_PATH" && ls -t | tail -n +6 | xargs -r rm -rf
        log "Old backups cleaned up"
    fi
else
    log "========================================"
    log "ERROR: Backup failed with exit code $EXIT_CODE"
    log "========================================"
    
    # Optional: Send notification
    if command -v notify-send &> /dev/null; then
        notify-send -u critical "KDE Plasma Backup Failed" "Check log: $LOG_FILE"
    fi
    
    exit 1
fi

# Optional: Send success notification
if [ "${SEND_NOTIFICATIONS:-false}" = "true" ]; then
    if command -v notify-send &> /dev/null; then
        notify-send -u normal "KDE Plasma Backup Complete" "Backup saved to NAS"
    fi
fi

exit 0
