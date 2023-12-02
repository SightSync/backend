import numpy as np

from gr_dino.GroundingDINO.groundingdino.util.inference import Model


class GroundingDinoMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(GroundingDinoMeta, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class GroundingDino(metaclass=GroundingDinoMeta):
    config_path = (
        "gr_dino/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"
    )
    checkpoint_path = "gr_dino/weights/groundingdino_swint_ogc.pth"
    model: Model

    def __init__(self):
        self.model = Model(
            model_config_path=self.config_path,
            model_checkpoint_path=self.checkpoint_path,
        )

    def predict(self, search_class: str, image: np.ndarray):
        detections = self.model.predict_with_classes(
            image=image,
            classes=[search_class],
            box_threshold=0.35,
            text_threshold=0.25,
        )
        print(detections)
        return detections
