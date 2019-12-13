class UnknownEditorException(Exception):
    pass


class CProgramClasses:
    _classes = {}

    @classmethod
    def register_new(cls, editor_name, editor_class):
        cls._classes[editor_name] = editor_class

    @classmethod
    def lookup_editor(cls, editor_name):
        if editor_name not in cls._classes:
            raise UnknownEditorException()
        return cls._classes[editor_name]

    @classmethod
    def editor_classes(cls):
        return [(editor_name, editor_class) for editor_name, editor_class in cls._classes.items()]


class CProgramMetaClass(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = super(CProgramMetaClass, cls).__new__(
            cls, clsname, bases, attrs)
        CProgramClasses.register_new(newclass.EDITOR, newclass)
        return newclass
