#!/bin/bash
# Diagnostic script to check backup contents

if [ -z "$1" ]; then
    echo "Usage: $0 <backup-directory>"
    echo "Example: $0 /home/mike/NAS/Backups/Fedora/KDE/MikeBookAir/20251211_153401"
    exit 1
fi

BACKUP_DIR="$1"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "Error: Directory does not exist: $BACKUP_DIR"
    exit 1
fi

echo "==================================="
echo "Backup Diagnostic Report"
echo "==================================="
echo ""
echo "Backup Directory: $BACKUP_DIR"
echo ""

# Check metadata
if [ -f "$BACKUP_DIR/backup_metadata.json" ]; then
    echo "✓ Metadata file exists"
    echo ""
    echo "Metadata contents:"
    cat "$BACKUP_DIR/backup_metadata.json" | python3 -m json.tool 2>/dev/null || cat "$BACKUP_DIR/backup_metadata.json"
    echo ""
else
    echo "✗ Metadata file missing"
    echo ""
fi

# Check directory structure
echo "Directory structure:"
find "$BACKUP_DIR" -maxdepth 2 -type d | sort
echo ""

# Count files in each directory
echo "File counts by directory:"
for dir in "$BACKUP_DIR"/*; do
    if [ -d "$dir" ]; then
        count=$(find "$dir" -type f | wc -l)
        dirname=$(basename "$dir")
        echo "  $dirname: $count files"
    fi
done
echo ""

# Check for empty directories
echo "Checking for empty directories:"
empty_count=0
for dir in $(find "$BACKUP_DIR" -type d); do
    if [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
        echo "  Empty: $dir"
        ((empty_count++))
    fi
done

if [ $empty_count -eq 0 ]; then
    echo "  No empty directories found"
fi
echo ""

# Size information
echo "Disk usage by component:"
du -sh "$BACKUP_DIR"/* 2>/dev/null | sort -hr
echo ""

echo "Total backup size:"
du -sh "$BACKUP_DIR"
echo ""

echo "==================================="
echo "Diagnostic complete"
echo "==================================="
