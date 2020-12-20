#!/usr/bin/env python3

import argparse
import subprocess
import sys
import tempfile

from markdown_it import MarkdownIt

__version__ = "0.1"


def runmd(text, language, command):
    md = MarkdownIt("commonmark")
    tokens = md.parse(text)
    code = "".join(
        t.content for t in tokens if t.type == "fence" and t.info.lower() == language
    )

    with tempfile.NamedTemporaryFile() as fp:
        fp.write(code.encode("UTF-8"))
        fp.seek(0)
        result = subprocess.run(command + [fp.name], check=False)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Concatenate tagged Markdown code fences and execute the result."
    )
    parser.add_argument("file", help="Markdown file to parse")
    args = parser.parse_args()

    with open(args.file) as f:
        text = f.read()

    sys.exit(runmd(text, "python", ["python3"]).returncode)
