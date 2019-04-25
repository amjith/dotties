#!/usr/bin/env python3

# Requires Python 3.7

import sys
import shutil
import os
import asyncio
from pathlib import Path

DOTTIES_FOLDER = Path.home() / '.dots'

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return stdout.decode(), stderr.decode()

async def _stow(name):
    try:
        cur_dir = os.getcwd()
        os.chdir(DOTTIES_FOLDER)
        print(f"stow {name}")
        out, err = await run(f"stow {name}")
        if err:
            print(err)
            return
        else:
            print(out)
    finally:
        os.chdir(cur_dir)

async def init():
    usage = '''Try,

dotties add path/to/folder_or_file
    or
"dotties scan" to scan and suggest dot files
    '''
    if DOTTIES_FOLDER.exists():
        print(f"{DOTTIES_FOLDER} already exists. " + usage)
        return

    a = input('Would you like to fetch your dotties from a git repo? (Y/N): ')
    if a.lower() == 'y':
        repo = input('git-url: ')
        out, err = await run(f"git clone {repo} {DOTTIES_FOLDER}")
        if err:
            print(err)
            return
        else:
            print(out)
            await _stow(".")
    else:
        os.makedirs(DOTTIES_FOLDER)
        os.chdir(DOTTIES_FOLDER)
        out, err = await run("git init")
        print(out or err)

def verify_init():
    if DOTTIES_FOLDER.exists():
        return True
    else:
        print(f"{DOTTIES_FOLDER} is missing. Run `dotties init`")
        sys.exit(1)

async def add(path_str):
    verify_init()
    src = Path(path_str)
    name = src.name if src.is_dir() else src.parent
    if src.is_file() and name.samefile(Path.home()):
        name = input('Name:')
    dest = DOTTIES_FOLDER / name / src.parent.relative_to(Path.home())
    os.makedirs(dest, exist_ok=True)
    # Check for already existing files before moving?
    print(f"Moving {src} to {dest}.")
    shutil.move(str(src), str(dest))
    print(f"Creating symlinks.")
    await _stow(name)

def sync():
    pass

def status():
    pass

def install():
    pass


COMMAND_HANDLERS = {
    "init": init,
    "add": add,
        }

async def main():
    handler = COMMAND_HANDLERS.get(sys.argv[1])
    if handler is None:
        print("unknown command")
    await handler(*sys.argv[2:])


if __name__ == '__main__':
    asyncio.run(main())
