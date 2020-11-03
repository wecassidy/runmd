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
   $ python3 runmd.py input_file.md
   Hello, world!
   Here's more code!
   3
   ```

## How it works

RunMD scans the input file for fenced code blocks with an info string
indicating the code is of a supported language (see
https://spec.commonmark.org/0.29/#fenced-code-blocks). It then
concatenates all code blocks of the same language into a temporary
file and executes that file.

If more than one supported language is present in the input file, the
languages are executed in the order they appear: for example, if the
first and third code blocks are in Python and the second is in Ruby,
first the Python file is run and then the Ruby. For obvious reasons,
it is a terrible idea to rely on this behaviour.
