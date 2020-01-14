import os

MAKE_C_EDITOR_ENV_VAR = "MAKE_C_EDITOR"
EDITOR_ENV_VAR = "EDITOR"
VISUAL_ENV_VAR = "VISUAL"


class EditorFromEnv:
    ENV_VAR_NAMES = [
        MAKE_C_EDITOR_ENV_VAR,
        EDITOR_ENV_VAR,
        VISUAL_ENV_VAR
    ]

    def __init__(self):
        self.editor = None
        self.path = None
        for env_var_name in self.ENV_VAR_NAMES:
            env_editor = os.environ.get(env_var_name)
            if env_editor:
                self.path = os.path.dirname(env_editor)
                self.editor = os.path.basename(env_editor)
                break
