# Chapter 0 — Your machine and your tools

| File | Step |
|:--|:--|
| `check_setup.py` | Step 9: checks every tool at once |

## Homebrew (macOS, Step 2)

Copy these two lines into the Terminal rather than typing them (the same lines as in the book):

```bash
BREW=https://raw.githubusercontent.com/Homebrew
/bin/bash -c "$(curl -fsSL $BREW/install/HEAD/install.sh)"
```

Then run the lines that Homebrew prints under *Next steps* (two start with `echo`, one with `eval`).

## Java on macOS (Step 6)

```bash
brew install openjdk@21
sudo ln -sfn $(brew --prefix)/opt/openjdk@21/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-21.jdk
echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 21)' >> ~/.zprofile
```

Open a new terminal afterwards, so that `JAVA_HOME` is set.

## Run the check

From the repository folder, with the virtual environment active:

```bash
python ch00-setup/check_setup.py
```

It ends with `All tools found` and exits with code 0, or lists each `MISSING` tool and exits with code 1.
