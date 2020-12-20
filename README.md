# RunMD

A script that concatenates all the code blocks in a Markdown file and
runs the resulting file.

## How to use

1. Write some Markdown with embedded code:
   ````markdown
   # Hello, world!
   ```python
   print("Hello, world!")
   x = 3
   ```
   Some text
   ```python
   print("Here's more code!")
   print(x)
   ```
   ````
2. Run the script
   ```bash
   $ python3 runmd.py input_file.md python --exec python3
   Hello, world!
   Here's more code!
   3
   ```

Untagged code blocks can be included with `--untagged`. Use `--exec
cmd` if the name of the language doesn't match the command to execute
it. `python3 runmd.py --help` for more information.

The error code of `runmd` is the same as the error code of the
executed script.

## How it works

RunMD scans the input file for fenced code blocks with an info string
indicating the correct language (see
https://spec.commonmark.org/0.29/#fenced-code-blocks). It then
concatenates all code blocks of that language into a temporary
file and executes that file.
