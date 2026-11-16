# Chapter 0 — Your machine and your tools

| File | Step |
|:--|:--|
| `check_setup.py` | Step 9: checks every tool at once |

## Homebrew (macOS, Step 2)

Copy this line into the Terminal rather than typing it:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then run the lines that Homebrew prints under *Next steps* (two start with `echo`, one with `eval`).

## Java on macOS (Step 6)

```bash
brew install openjdk@21
sudo ln -sfn $(brew --prefix)/opt/openjdk@21/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-21.jdk
```

## Run the check

From the repository folder, with the virtual environment active:

```bash
python ch00-setup/check_setup.py
```
