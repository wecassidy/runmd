#!/usr/bin/env python3

import argparse
import subprocess
import sys
import tempfile

from markdown_it import MarkdownIt

__version__ = "0.2"


def build_command(command, name):
    """
    Insert a filename into an executable command where appropriate.
    """
    return command + " " + name


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
    parser.add_argument(
        "-l", "--lang", metavar=("language", "command"), nargs=2, help="blah"
    )
    args = parser.parse_args()

    with open(args.file) as f:
        text = f.read()

    lang = args.lang if args.lang is not None else ("python", "python3")

    sys.exit(runmd(text, *lang).returncode)
