import os


class EditorFromEnv:
    def __init__(self):
        self.editor = None
        self.path = None
        env_editor = os.environ.get("EDITOR")
        if env_editor:
            self.path = os.path.dirname(env_editor)
            self.editor = os.path.basename(env_editor)
