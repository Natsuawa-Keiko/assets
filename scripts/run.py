#!/usr/bin/env python

import argparse
import subprocess
from pathlib import Path

import pyperclip
from hash_rename import rename

PREFIX = 'https://media.githubusercontent.com/media'
ACCOUNT = 'Natsuawa-Keiko'
REPOSITORY = 'assets'
BRANCH = 'main'

DIRS = [
    './images/general/',
    './images/chat_log/',
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--force-all', action='store_true')
    options = parser.parse_args()

    force_all = options.force_all

    files: list[Path] = []

    for dir in DIRS:
        for i in Path(dir).rglob('*'):
            if not i.is_file():
                continue
            if not force_all:
                if (
                    i.stem.isalnum()
                    and len(i.stem) == 64
                    and i.name.islower()
                ):
                    continue
            files.append(i)

    clipboard: list[str] = []

    for i in Path(__file__).resolve().parents:
        if i.name == 'scripts':
            root = i.parent
            break

    for file in files:
        i = rename(file).pop(file).resolve().relative_to(root).as_posix()
        clipboard.append(
            f'![]({PREFIX}/{ACCOUNT}/{REPOSITORY}/{BRANCH}/{i})'
        )

    pyperclip.copy('\n\n'.join(clipboard))

    subprocess.run('git add -A')
    subprocess.run('git commit -q -m "Upload"')
    subprocess.run('git push -f')


if __name__ == '__main__':
    main()
