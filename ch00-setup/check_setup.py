"""Chapter 0 — check that every tool used in the book is installed.

Run from the repository folder, with the virtual environment active:
    python ch00-setup/check_setup.py

The script exits with code 0 when every tool is found, and 1 when one is missing.

MERIDIAN_SKIP (for automated tests only, not for readers): a comma-separated list
of tool names, as printed in the first column, that the machine running the test
does not install, for example MERIDIAN_SKIP="R,docker". A skipped tool that is
missing prints SKIPPED and does not count as missing. Readers leave it unset.
"""
import os
import re
import shutil
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version


def command_version(cmd, pattern):
    """Run a command and pull the version number out of its output."""
    if shutil.which(cmd[0]) is None:
        return None
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    match = re.search(pattern, out.stdout + out.stderr)
    return match.group(1) if match else None


def package_version(name):
    try:
        return version(name)
    except PackageNotFoundError:
        return None


checks = [
    ('Python',   '{}.{}.{}'.format(*sys.version_info[:3])),
    ('pandas',   package_version('pandas')),
    ('pyspark',  package_version('pyspark')),
    ('dbt-core', package_version('dbt-core')),
    ('psql',     command_version(['psql', '--version'], r'(\d+\.\d+)')),
    ('java',     command_version(['java', '-version'], r'version "(\d+\.\d+\.\d+)')),
    ('R',        command_version(['R', '--version'], r'R version (\d+\.\d+\.\d+)')),
    ('git',      command_version(['git', '--version'], r'(\d+\.\d+\.\d+)')),
    ('docker',   command_version(['docker', '--version'], r'(\d+\.\d+\.\d+)')),
]

skipped = {name.strip().lower()
           for name in os.environ.get('MERIDIAN_SKIP', '').split(',') if name.strip()}

missing = 0
for name, found in checks:
    if found:
        print(f'{name:<11} {found:<9} OK')
    elif name.lower() in skipped:
        print(f'{name:<11} {"":<9} SKIPPED')
    else:
        print(f'{name:<11} {"":<9} MISSING')
        missing += 1

if missing:
    print(f'{missing} tool(s) missing. Repeat the matching step of Chapter 0.')
    sys.exit(1)
print('All tools found. You are ready for Chapter 1.')
