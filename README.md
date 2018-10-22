# make_c

A script to generate a simple C program with a few basic includes and a `main()`. Then it opens the file in your editor of choice placing the cursor at the proper line and column to start adding code.

Supported editors include:

- vim
- SublimeText (`subl`)

### Adding editor support

To add additional editors, extend the `CProgram` class and override:

- the `EDITOR` class variable
- The `open_in_editor()` instance method

The `open_in_editor()` method should return an `argv` that represents that editor's commandline incantation in list form suitable for consumption by `subprocess.Popen()`. For example, if your editor takes a `--line` and `--column` argument, you would return:

```python
[self.EDITOR,
    "--line",
    "%d" % self.edit_line,
    "--column",
    "%d" % self.edit_column,
    self.filename]
```

