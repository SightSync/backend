import cv2
from models.grouding_dino import GroundingDino
from services.image import UPLOAD_IMG_DIR


class LocateService:
    grounding_dino: GroundingDino

    def __init__(self):
        self.grounding_dino = GroundingDino()

    def predict(self, img_name: str, class_name: str):
        image = cv2.imread(f"{UPLOAD_IMG_DIR}/{img_name}")
        return self.grounding_dino.predict(class_name, image)
