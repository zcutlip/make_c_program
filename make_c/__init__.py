from .__about__ import (
    __version__,
    __title__,
    __summary__
)
from .editors import CProgramClasses
from .meta import UnknownEditorException

__all__ = [
    "__version__",
    "__title__",
    "__summary__",
    CProgramClasses,
    UnknownEditorException
]
