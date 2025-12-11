# Contributing to KDE Plasma Backup Manager

Thank you for your interest in contributing! This project is a community effort to provide a reliable backup solution for KDE Plasma users.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## Code of Conduct

This project follows the KDE Community Code of Conduct. Please be respectful and constructive in all interactions.

## How Can I Contribute?

### 1. Testing

- Test the application on different Fedora versions
- Test on other Linux distributions (Ubuntu, openSUSE, etc.)
- Test with different KDE Plasma versions
- Report bugs and issues you encounter

### 2. Bug Fixes

- Fix reported bugs from the issue tracker
- Improve error handling
- Add missing validation

### 3. Features

Priority features for contribution:
- **Compression support** - Add tar.gz/zip compression
- **Incremental backups** - Only backup changed files
- **Encryption** - Encrypt backup archives
- **GUI translations** - Translate the interface to other languages
- **Steam integration** - Backup Steam library and saves
- **Lutris integration** - Backup Lutris game configurations
- **Selective restore** - Restore only specific files/directories
- **Backup comparison** - Compare two backups to see differences

### 4. Documentation

- Improve existing documentation
- Add screenshots
- Create video tutorials
- Translate documentation
- Add troubleshooting guides for specific scenarios

### 5. Testing on Other Distributions

We'd love to support more distributions:
- Ubuntu with KDE Plasma
- openSUSE Tumbleweed
- Arch Linux
- Manjaro
- KDE neon

## Development Setup

### Prerequisites

- Fedora Linux (or compatible distribution)
- KDE Plasma 6.5+
- Python 3.9+
- Git
- Basic knowledge of Python and Qt

### Setting Up Development Environment

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/KDE-Plasma-Backup-Manager.git
cd KDE-Plasma-Backup-Manager

# 3. Add upstream remote
git remote add upstream https://github.com/alduccino/KDE-Plasma-Backup-Manager.git

# 4. Install dependencies
sudo dnf install python3 python3-pip qt6-qtbase
pip install --user -r requirements.txt

# 5. Create a development branch
git checkout -b feature/your-feature-name

# 6. Make your changes

# 7. Test your changes
./plasma-backup-manager.py
./plasma-backup-cli.py --help
```

### Project Structure

```
KDE-Plasma-Backup-Manager/
├── plasma-backup-manager.py    # Main GUI application
├── plasma-backup-cli.py         # CLI version
├── plasma-backup-auto.sh        # Automation wrapper
├── install.sh                   # Installation script
├── requirements.txt             # Python dependencies
├── README.md                    # Main documentation
├── QUICKSTART.md                # Quick start guide
├── CONTRIBUTING.md              # This file
├── CHANGELOG.md                 # Version history
├── LICENSE                      # GPL-3.0 license
└── docs/                        # Additional documentation
```

## Coding Guidelines

### Python Code Style

- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable and function names
- Add docstrings to all functions and classes

Example:
```python
def backup_kde_settings(self, backup_dir):
    """
    Backup KDE Plasma settings including plasmoids.
    
    Args:
        backup_dir: Path object pointing to backup directory
    
    Returns:
        bool: True if successful, False otherwise
    """
    self.log("Backing up KDE Plasma settings...")
    # Implementation
```

### Qt/PyQt6 Guidelines

- Use Qt6 widgets and APIs
- Follow Qt naming conventions (camelCase for methods)
- Keep UI code separate from business logic
- Use QThread for long-running operations
- Emit signals for progress updates

### Shell Script Guidelines

- Use bash for shell scripts
- Set `set -e` for error handling
- Add comments for complex operations
- Use consistent indentation
- Validate inputs and check for errors

### Commit Messages

Format:
```
type: Brief description (max 50 chars)

Detailed explanation if needed (max 72 chars per line)

Fixes: #issue-number
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat: Add compression support for backups

Implements tar.gz compression using tarfile module.
Users can now choose to compress backups to save space.

Fixes: #42
```

```
fix: Handle missing XDG user directories gracefully

Previously crashed if user-dirs.dirs was missing.
Now falls back to default directory names.

Fixes: #38
```

## Submitting Changes

### Pull Request Process

1. **Update from upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test your changes thoroughly**
   - Test GUI functionality
   - Test CLI functionality
   - Test on a clean Fedora installation if possible
   - Verify no regressions

3. **Update documentation**
   - Update README.md if adding features
   - Update CHANGELOG.md
   - Add comments to complex code

4. **Create Pull Request**
   - Push to your fork
   - Create PR on GitHub
   - Fill out the PR template
   - Link related issues

5. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Code refactoring
   
   ## Testing
   How was this tested?
   
   ## Screenshots (if applicable)
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] Changes tested
   - [ ] No breaking changes (or documented)
   
   ## Related Issues
   Fixes: #issue-number
   ```

### Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged
- Your contribution will be credited in CHANGELOG.md

## Reporting Bugs

### Before Reporting

1. Check if the bug is already reported in [GitHub Issues](https://github.com/alduccino/KDE-Plasma-Backup-Manager/issues)
2. Test on the latest version
3. Gather necessary information

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**System Information**
- OS: Fedora 43
- KDE Plasma Version: 6.5.1
- Python Version: 3.12
- Application Version: 1.0.0

**Logs**
```
Paste relevant logs here
```

**Screenshots**
If applicable
```

## Suggesting Features

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Problem It Solves**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other ways to solve this?

**Additional Context**
Any other relevant information
```

## Priority Areas

We especially welcome contributions in these areas:

### High Priority
- Compression support
- Incremental backup functionality
- GUI translations
- Testing on other distributions

### Medium Priority
- Backup encryption
- Steam/Lutris integration
- Selective restore
- Backup comparison tool

### Low Priority
- Custom backup profiles
- Cloud storage integration
- Web interface
- Mobile companion app

## Getting Help

- **GitHub Discussions**: Ask questions
- **GitHub Issues**: Report bugs or request features
- **Email**: Contact maintainers directly (see README)

## Recognition

Contributors will be:
- Listed in CHANGELOG.md
- Credited in release notes
- Acknowledged in the project README

Thank you for contributing to KDE Plasma Backup Manager! 🎉
