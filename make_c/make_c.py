#!/usr/bin/env python

import argparse
import subprocess
import sys

CProgramClasses={}

def register(cls):
    newclass=cls
    CProgramClasses[newclass.EDITOR]=newclass
    return newclass

class CProgramMetaClass(type):
    def __new__(cls,clsname,bases,attrs):
        newclass=super(CProgramMetaClass,cls).__new__(cls,clsname,bases,attrs)
        register(newclass)
        return newclass

class CProgram(object):
    __metaclass__=CProgramMetaClass
    FOURSPACES="    "
    TAB="\t"
    INSERT_CODE_HERE="//insert code here"
    EDITOR="vim"
    def __init__(self,filename,spaces=True,run_editor=True):
        self.filename=filename
        if spaces:
            tab=self.FOURSPACES
        else:
            tab=self.TAB

        self.insert_code_comment=tab+self.INSERT_CODE_HERE
        lines= ["#include <stdlib.h>",
                "#include <stdio.h>",
                "#include <unistd.h>",
                "#include <string.h>",
                "",
                "",
                "int main(int argc, char **argv)",
                "{",
                tab+"int ret=0;",
                "",
                tab+"printf(\"Hello world\\n\");",
                self.insert_code_comment, #so we can dyanmically locate its index later
                "",
                tab+"return ret;",
                "}",
                ""]
        self.lines=lines
        self.edit_line=self.lines.index(self.insert_code_comment)+1
        self.edit_column=len(tab)+1

        self._write_to_file()
        if run_editor:
            self.open_in_editor()

    def _write_to_file(self):
        try:
            with open(self.filename,"w") as outfile:
                for line in self.lines:
                    outfile.write(line+"\n")

        except Exception as e:
            print("Error writing %s" % self.filename)
            print("%s" % str(e))

    def generate_editor_command(self):
        line_column_arg="+call cursor(%d,%d)" % (self.edit_line,self.edit_column)

        #vim foo.c "+call cursor(4,5)"
        return[self.EDITOR,line_column_arg,self.filename]
    
    def open_in_editor(self):
        p=subprocess.Popen(self.generate_editor_command())
        p.wait()

class CProgramWithSublime(CProgram):
    EDITOR="subl"
    def generate_editor_command(self):
        line_column_arg=":%d:%d" % (self.edit_line,self.edit_column)

        #subl foo.c:4:5
        editor_cmd=[self.EDITOR,self.filename+line_column_arg]
        
        return editor_cmd

class CProgramWithTextMate(CProgram):
    EDITOR="mate"

    def generate_editor_command(self):
        line_column_arg="%d:%d" % (self.edit_line,self.edit_column)
        editor_cmd=[self.EDITOR,"-l",line_column_arg,self.filename]
        return editor_cmd

def list_editors():
    print("Known editors:")
    for editor in CProgramClasses.keys():
        print("%s" % editor)

def parse_args(argv):
    parser=argparse.ArgumentParser()
    grp=parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("filename",nargs='?',help="Name of the source file to create.",default=None)
    grp.add_argument("--list-editors",help="List known editors.",action="store_true",default=False)
    parser.add_argument("--editor",help="Editor to use to open the resulting source file.")
    parser.add_argument("--skip-editor",help="Create the source file but don't open it in an editor.",action="store_true")
    parser.add_argument("--tabs",help="Use tabs instead of spaces.",action="store_true")

    args=parser.parse_args(argv)
    return args

def main(argv):
    args=parse_args(argv)
    run_editor=True

    if args.list_editors:
        list_editors()
        exit(0)


    run_editor=not args.skip_editor

    filename=args.filename
    
    editor="vim"
    if args.editor:
        editor=args.editor

    spaces=not args.tabs

    try:
        c_program_class=CProgramClasses[editor]
    except:
        print("Unknown editor: %s" % editor)
        print("Consider using --skip-editor to create source file without editing.")
        exit(1)


     #def __init__(self,filename,spaces=True,run_editor=True):
    c_program_class(filename,spaces=spaces,run_editor=run_editor)

if __name__=="__main__":
    main(sys.argv[1:])



