# PyShell

Command line interpreter implemented in Python.

## Supported commands

Built-in commands

- bg
- cd [dir]
- pwd
- time command
- clr
- dir [dir]
- environ
- echo [comment]
- help
- quit
- fg
- jobs
- set var val
- shift
- test
- umask [mask]
- unset var

Use `help` for more detail.

Program execution from the shell is supported without doubt.

## Features

Redirection (works only for built-in commands)

```sh
echo hello > hello.txt
```

Pipeline

```sh
cat shell.py | wc
```

Background execution

```sh
sleep 10 & sleep 5 &
```

Batchfile

```sh
python shell.py BATCHFILE
```
