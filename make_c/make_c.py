#!/usr/bin/env python3

import argparse
import sys

from .version import MakeCAbout
from . import CProgramClasses, UnknownEditorException
from .environment import EditorFromEnv
from .editors import DEFAULT_EDITOR


def list_editors():
    print("Known editors:\n")
    for _, editor_cls in CProgramClasses.editor_classes():
        print("%s" % editor_cls.description())


def parse_args(argv):
    description = str(MakeCAbout())
    parser = argparse.ArgumentParser(description=description)
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("filename", nargs='?',
                     help="Name of the source file to create.", default=None)
    grp.add_argument("--list-editors", help="List known editors.",
                     action="store_true", default=False)
    parser.add_argument("--version", help="Print version string and exit.",
                        action="version",
                        version=description)
    parser.add_argument(
        "--editor", help="Editor to use to open the resulting source file.")
    parser.add_argument(
        "--skip-editor", help="Create the source file but don't open it in an editor.", action="store_true")
    parser.add_argument(
        "--tabs", help="Use tabs instead of spaces.", action="store_true")
    parser.add_argument("--generate-makefile",
                        help="Create a makefile to build the program.", action="store_true")

    args = parser.parse_args(argv)
    return args


def main(argv):
    args = parse_args(argv)
    run_editor = True

    if args.list_editors:
        list_editors()
        exit(0)

    run_editor = not args.skip_editor

    filename = args.filename

    editor = args.editor
    editor_path = None
    if not editor:
        env_editor = EditorFromEnv()
        editor = env_editor.editor
        editor_path = env_editor.path
    if not editor:
        editor = DEFAULT_EDITOR

    spaces = not args.tabs
    generate_makefile = args.generate_makefile
    try:
        c_program_class = CProgramClasses.lookup_editor(editor)
    except UnknownEditorException:
        print("Unknown editor: %s" % editor)
        print("Consider using --skip-editor to create source file without editing.")
        exit(1)

    c_program_class(filename,
                    spaces=spaces,
                    generate_makefile=generate_makefile,
                    run_editor=run_editor,
                    path_to_editor=editor_path)


if __name__ == "__main__":
    main(sys.argv[1:])
