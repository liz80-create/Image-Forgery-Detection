from .imageforensics import ImageForensics

class SplicingForensics(ImageForensics):
    def __init__(self, model_path, class_names):
        super().__init__(model_path, class_names)
        self.image_size = (128, 128)