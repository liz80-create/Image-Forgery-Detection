from .imageforensics import ImageForensics

class CopyMoveForensics(ImageForensics):
    def __init__(self, model_path, class_names):
        super().__init__(model_path, class_names)