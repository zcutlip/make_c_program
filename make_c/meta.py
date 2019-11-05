CProgramClasses = {}


def register(cls):
    newclass = cls
    CProgramClasses[newclass.EDITOR] = newclass
    return newclass


class CProgramMetaClass(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = super(CProgramMetaClass, cls).__new__(
            cls, clsname, bases, attrs)
        register(newclass)
        return newclass
