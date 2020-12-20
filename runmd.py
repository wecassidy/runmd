#!/usr/bin/env python3

import argparse
import subprocess
import sys
import tempfile

from markdown_it import MarkdownIt

__version__ = "0.3"


def build_command(command, name):
    """
    Insert a filename into an executable command where appropriate.

    The command uses a simplified case of printf-style substitution:
    each %s is replaced with the filename. To escape a %, use %%. All
    other %* are ignored. If no %s is present, the name is appended to
    the command.
    """
    cmd = ""
    last_mod = False
    no_sub = True
    for i, char in enumerate(command):
        if last_mod:
            last_mod = False
            if char == "s":
                cmd += name
                no_sub = False
            elif char == "%":
                cmd += "%"
            else:
                cmd += "%" + char
        elif char != "%":
            cmd += char
        else:
            last_mod = True
    if last_mod:
        cmd += "%"

    if no_sub:
        cmd += " " + name

    return cmd


def runmd(text, language, command):
    md = MarkdownIt("commonmark")
    tokens = md.parse(text)
    code = "".join(
        t.content for t in tokens if t.type == "fence" and t.info.lower() == language
    )

    with tempfile.NamedTemporaryFile() as fp:
        fp.write(code.encode("UTF-8"))
        fp.seek(0)
        result = subprocess.run(
            build_command(command, fp.name), check=False, shell=True
        )

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Concatenate tagged Markdown code fences and execute the result."
    )
    parser.add_argument("file", help="Markdown file to parse")
    parser.add_argument("language", help="Language to run")
    parser.add_argument(
        "-e",
        "--exec",
        metavar="command",
        help="Command to execute the concatenated code. If not specified, the language will be used.",
    )
    args = parser.parse_args()

    with open(args.file) as f:
        text = f.read()

    cmd = args.exec if args.exec is not None else args.language

    sys.exit(runmd(text, args.language, cmd).returncode)
