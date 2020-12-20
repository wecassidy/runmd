#!/usr/bin/env python3

import argparse
import subprocess
import sys
import tempfile
import textwrap

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


def check_language_tag(token, lang, include_untagged):
    return token.info == lang or (include_untagged and token.info == "")


def runmd(text, language, command, include_untagged):
    md = MarkdownIt("commonmark")
    tokens = md.parse(text)
    code = "".join(
        t.content
        for t in tokens
        if t.type == "fence" and check_language_tag(t, language, include_untagged)
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
        description="""
                    Concatenate tagged Markdown code fences and
                    execute the result. The error code of runmd is the
                    same as the error code of the executed code.
                    """,
        epilog=textwrap.dedent(
            """
            EXEC EXAMPLES
              No --exec: -> `language tempfile`

              Appending: `--exec cmd` -> `cmd tempfile`

              Substitution: `--exec 'cmd %s --format "%s %d %%s"` -> `cmd tempfile --format "tempfile %d %s"`
            """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "file",
        help="Markdown file to parse for code blocks. runmd expects a Commonmark-compliant file.",
    )
    parser.add_argument("language", help="Language to extract")
    parser.add_argument(
        "-e",
        "--exec",
        metavar="command",
        # I'm sorry for the % pileup, but it turns out argparse uses
        # printf-style formatting internally so they must be escaped.
        help="""
             Command to execute the concatenated code. If not
             specified, the language name will be used as the command.
             By default, the temporary file concatenated code is added
             as the last argument to the script. Alternatively, a
             simple printf-like format can be used: all occurences of
             %%s are replaced by the temporary file containing the
             concatenated code. All other %%* are ignored. Use %% to
             escape a %%: "%%%%s" becomes "%%s" rather than "%%temp_file".
             See EXEC EXAMPLES.
             """,
    )
    parser.add_argument(
        "-u", "--untagged", action="store_true", help="Include untagged blocks"
    )
    args = parser.parse_args()

    with open(args.file) as f:
        text = f.read()

    cmd = args.exec if args.exec is not None else args.language

    sys.exit(runmd(text, args.language, cmd, args.untagged).returncode)
