#!/bin/bash
# Test script to diagnose NAS copy issues

echo "==================================="
echo "NAS Copy Diagnostics"
echo "==================================="
echo ""

# Test location
TEST_DIR="${1:-$HOME/NAS/Backups/test-$(date +%s)}"
echo "Test directory: $TEST_DIR"
echo ""

# Create test directory
echo "Creating test directory..."
if mkdir -p "$TEST_DIR" 2>/dev/null; then
    echo "✓ Directory creation successful"
else
    echo "✗ Failed to create directory"
    exit 1
fi
echo ""

# Test 1: Simple file copy
echo "Test 1: Simple file copy with cp"
TEST_FILE="$HOME/.bashrc"
if [ -f "$TEST_FILE" ]; then
    if cp "$TEST_FILE" "$TEST_DIR/test1.txt" 2>/dev/null; then
        echo "✓ Simple cp works"
    else
        echo "✗ Simple cp failed"
    fi
else
    echo "Creating test file..."
    echo "test" > /tmp/test.txt
    if cp /tmp/test.txt "$TEST_DIR/test1.txt" 2>/dev/null; then
        echo "✓ Simple cp works"
    else
        echo "✗ Simple cp failed"
    fi
fi
echo ""

# Test 2: Copy with Python shutil.copy2
echo "Test 2: Copy with Python shutil.copy2"
python3 << 'EOF'
import shutil
try:
    shutil.copy2('/tmp/test.txt', '$TEST_DIR/test2.txt')
    print("✓ Python shutil.copy2 works")
except Exception as e:
    print(f"✗ Python shutil.copy2 failed: {e}")
EOF
echo ""

# Test 3: Copy without preserving metadata
echo "Test 3: Copy without preserving metadata"
if cp --no-preserve=all /tmp/test.txt "$TEST_DIR/test3.txt" 2>/dev/null; then
    echo "✓ Copy without metadata preservation works"
else
    echo "✗ Copy without metadata preservation failed"
fi
echo ""

# Test 4: Check NFS mount options
echo "Test 4: NFS Mount Information"
if mount | grep -i nfs | grep "$(df "$TEST_DIR" | tail -1 | awk '{print $1}')"; then
    echo "NFS mount found"
else
    echo "Not an NFS mount (or mount info not available)"
fi
echo ""

# Test 5: Check file attributes
echo "Test 5: Source file attributes"
if [ -f "$HOME/.config/plasmarc" ]; then
    ls -la "$HOME/.config/plasmarc"
    echo ""
    echo "Extended attributes:"
    getfattr -d "$HOME/.config/plasmarc" 2>/dev/null || echo "No extended attributes or getfattr not available"
fi
echo ""

# Cleanup
echo "Cleaning up test directory..."
rm -rf "$TEST_DIR"
echo "Done"
echo ""

echo "==================================="
echo "Recommendations:"
echo "==================================="
echo ""
echo "If simple cp works but shutil.copy2 fails:"
echo "  → Issue is with metadata preservation"
echo "  → Solution: Use shutil.copy() instead of shutil.copy2()"
echo ""
echo "If nothing works:"
echo "  → NFS mount may need different options"
echo "  → Check /etc/fstab for: no_root_squash, all_squash settings"
echo "  → Try remounting with: sudo mount -o remount,nfsvers=3 ~/NAS"
echo ""
