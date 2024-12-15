# Some methods have empty implementation here because they are implemented in
# `shell.py`. They are listed here only for documentation purposes.

import os
import sys

def bg(jid):
    """
    SYNOPSIS
        bg jid

    DESCRIPTION
        Move job to the background.
    """
    pass

def cd(path='.'):
    """
    SYNOPSIS
        cd PATH

    DESCRIPTION
        Change directory.
    """
    try:
        os.chdir(os.path.abspath(path))
    except FileNotFoundError:
        print(f'cd: no such directory: {path}')
    except NotADirectoryError:
        print(f'cd: not a directory: {path}')

def clr():
    """
    SYNOPSIS
        clr

    DESCRIPTION
        Clear screen.
    """
    os.system('clear')

def dir(path='.'):
    """
    SYNOPSIS
        dir [PATH]

    DESCRIPTION
        List directory contents. List pwd if the PATH is not provided.
    """
    try:
        print('  '.join(os.listdir(path)))
    except FileNotFoundError:
        print(f'dir: no such directory: {path}')
    except NotADirectoryError:
        print(f'dir: not a directory: {path}')

def echo(*comment):
    """
    SYNOPSIS
        echo [STRING]

    DESCRIPTION
        Display a line of text.
    """
    print(' '.join(comment))

def exec():
    """
    SYNOPSIS
    DESCRIPTION
    """
    pass

def exit():
    """
    SYNOPSIS
        exit

    DESCRIPTION
        Exit from shell.
    """
    return True

def environ():
    """
    SYNOPSIS
        environ

    DESCRIPTION
        List all environment variables.
    """
    pass

def fg():
    """
    SYNOPSIS
        fg

    DESCRIPTION
        Move job to the foreground.
    """
    pass

def helpsh():
    """
    SYNOPSIS
        help/helpsh

    DESCRIPTION
        Show the manual of psh commands.
    """
    help(sys.modules[__name__])

def jobs():
    """
    SYNOPSIS
        jobs

    DESCRIPTION
        Display status of jobs.
    """
    pass

def pwd():
    """
    SYNOPSIS
        pwd

    DESCRIPTION
        Print name of working directory.
    """
    print(os.getcwd())

def quit():
    """
    SYNOPSIS
        quit

    DESCRIPTION
        Quit shell.
    """
    return True

def set(var, val):
    """
    SYNOPSIS
        set VAR VAL

    DESCRIPTION
        Set the value of environment variables.
    """
    pass

def shift(self):
    """
    SYNOPSIS
        shift [n]

    DESCRIPTION
        Shift positional parameters.
    """
    pass

def test(self):
    """
    SYNOPSIS
    DESCRIPTION
    """
    pass

def time(function, *args):
    """
    SYNOPSIS
        time COMMAND

    DESCRIPTION
        Get the real, user and sys time of the execution of the COMMAND.
    """
    from resource import getrusage, RUSAGE_SELF
    from time import time as timestamp

    start_time, start_resources = timestamp(), getrusage(RUSAGE_SELF)
    try:
        eval(function)(*args)
    except NameError:
        print(f'time: no such command: {function}')
    end_resources, end_time = getrusage(RUSAGE_SELF), timestamp()

    print()
    print(f'real {(end_time - start_time):.5f}s')
    print(f'user {(end_resources.ru_utime - start_resources.ru_utime):.5f}s')
    print(f'sys  {(end_resources.ru_stime - start_resources.ru_stime):.5f}s')

def umask(mask=None):
    """
    SYNOPSIS
        umask [MASK]

    DESCRIPTION
        Display or set file mode mask.
    """
    if mask:
        os.umask(int(mask, 8))
    else:
        omask = os.umask(0)
        print(f'{omask:04o}')
        os.umask(omask)

def unset(var):
    """
    SYNOPSIS
        unset VAR

    DESCRIPTION
        Unset an environment variable.
    """
    pass
