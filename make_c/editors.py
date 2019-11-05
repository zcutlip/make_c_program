import os
import subprocess
from pprint import pprint
from .meta import CProgramMetaClass, CProgramClasses


class CProgram(metaclass=CProgramMetaClass):
    FOURSPACES = "    "
    TAB = "\t"
    INSERT_CODE_HERE = "//insert code here"
    EDITOR = "vim"
    DESCRIPTION = "Vi IMproved, a programmer's text editor"

    def __init__(self, filename, spaces=True, generate_makefile=False, run_editor=True):
        self.filename = filename
        if spaces:
            tab = self.FOURSPACES
        else:
            tab = self.TAB

        self.insert_code_comment = tab + self.INSERT_CODE_HERE
        lines = ["#include <stdlib.h>",
                 "#include <stdio.h>",
                 "#include <unistd.h>",
                 "#include <string.h>",
                 "",
                 "",
                 "int main(int argc, char **argv)",
                 "{",
                 tab + "int ret=0;",
                 "",
                 tab + "printf(\"Hello world\\n\");",
                 self.insert_code_comment,  # so we can dyanmically locate its index later
                 "",
                 tab + "return ret;",
                 "}",
                 ""]
        self.lines = lines
        self.edit_line = self.lines.index(self.insert_code_comment) + 1
        self.edit_column = len(tab) + 1

        self._write_to_file(self.filename, self.lines)
        if generate_makefile:
            self.makefile_lines = self._generate_makefile()
            self._write_to_file("Makefile", self.makefile_lines)

        if run_editor:
            self.open_in_editor()

    def _write_to_file(self, filename, lines):
        try:
            with open(filename, "w") as outfile:
                for line in lines:
                    outfile.write(line + "\n")

        except Exception as e:
            print("Error writing %s" % self.filename)
            print("%s" % str(e))
            raise

    def _generate_makefile(self):
        basename = os.path.splitext(self.filename)[0]

        lines = ["%s:%s" % (basename, self.filename),
                 "\tcc $^ -o $@",
                 "",
                 "clean:",
                 "\t-rm -f %s" % basename,
                 ""]

        return lines

    def generate_editor_command(self):
        line_column_arg = "+call cursor(%d,%d)" % (self.edit_line,
                                                   self.edit_column)

        # vim foo.c "+call cursor(4,5)"
        return[self.EDITOR, line_column_arg, self.filename]

    def open_in_editor(self):
        p = subprocess.Popen(self.generate_editor_command())
        p.wait()

    @classmethod
    def description(cls):
        return "%s: %s" % (cls.EDITOR, cls.DESCRIPTION)


class CProgramWithSublime(CProgram):
    EDITOR = "subl"
    DESCRIPTION = "Sublime Text 3"

    def generate_editor_command(self):
        line_column_arg = ":%d:%d" % (self.edit_line, self.edit_column)

        # subl foo.c:4:5
        editor_cmd = [self.EDITOR, self.filename + line_column_arg]

        return editor_cmd


class CProgramWithTextMate(CProgram):
    EDITOR = "mate"
    DESCRIPTION = "TextMate 2"

    def generate_editor_command(self):
        line_column_arg = "%d:%d" % (self.edit_line, self.edit_column)

        # mate -l 4:5 foo.c
        editor_cmd = [self.EDITOR, "-l", line_column_arg, self.filename]
        return editor_cmd


class CProgramWithVSCode(CProgram):
    EDITOR = "code"
    DESCRIPTION = "Visual Studio Code"

    def generate_editor_command(self):
        path = os.path.dirname(self.filename)
        path = os.path.expanduser(path)
        path = os.path.realpath(path)
        file_line_arg = "%s:%s:%d" % (self.filename, self.edit_line, self.edit_column)
        editor_cmd = [self.EDITOR, "-n", path, "-g", file_line_arg]
        pprint(editor_cmd)
        return editor_cmd
