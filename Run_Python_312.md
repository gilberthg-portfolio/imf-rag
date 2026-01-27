# Running Python 3.12

## Quick Reference

```bash
# Check Python 3.12 is installed
py -3.12 --version

# Create virtual environment
py -3.12 -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Verify correct version
python --version

# Install packages (use python -m pip to avoid permission issues)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Or install packages directly
python -m pip install package_name

# Deactivate when done
deactivate
```

## Why use `python -m pip` instead of `pip`?

Using `python -m pip` runs pip as a module through the Python interpreter, bypassing the `.exe` file. This avoids "Access is denied" errors that can occur after pip upgrades.

## Multiple Python Versions

```bash
py -3.12 -m venv venv312    # Python 3.12 environment
py -3.14 -m venv venv314    # Python 3.14 environment
```

Each venv is independent. Activate whichever you need.
