# make_c

A script to generate a simple C program with a few basic includes and a `main()`. Then it opens the file in your editor of choice placing the cursor at the proper line and column to start adding code.

Supported editors include:

- vim
- SublimeText (`subl`)
- TextMate (`mate`)

### Installing

```
$ cd make_c
$ python setup.py install
```

### Running

Help output:
```
$ make_c.py -h

usage: make_c [-h] [--editor EDITOR] [--list-editors] [--skip-editor] [--tabs]
              filename

positional arguments:
  filename         Name of the source file to create.

optional arguments:
  -h, --help       show this help message and exit
  --editor EDITOR  Editor to use to open the resulting source file.
  --list-editors   List known editors.
  --skip-editor    Create the source file but don't open it in an editor.
  --tabs           Use tabs instead of spaces.
```

Creating and editing a file:

```
make_c foo.c

#Edit in SublimeText instead:

make_c foo.c --editor=subl
```
### Adding editor support

To add additional editors, extend the `CProgram` class and override:

- the `EDITOR` class variable
- The `generate_editor_command()` instance method

The `generate_editor_command()` method should return an `argv` that represents that editor's commandline incantation in list form suitable for consumption by `subprocess.Popen()`. For example, if your editor takes a `--line` and `--column` argument, you would return:

```python
def generate_editor_command(self):
    return [self.EDITOR,
            "--line",
            "%d" % self.edit_line,
            "--column",
            "%d" % self.edit_column,
            self.filename]
```

