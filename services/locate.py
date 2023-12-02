import cv2
import numpy as np

from models.grouding_dino import GroundingDino
from schemas.direction import Direction
from services.image import UPLOAD_IMG_DIR


class LocateService:
    grounding_dino: GroundingDino

    def __init__(self):
        self.grounding_dino = GroundingDino()

    def predict(self, img_name: str, class_name: str):
        image = cv2.imread(f"{UPLOAD_IMG_DIR}/{img_name}")
        coordinates = self.grounding_dino.predict(class_name, image)
        print(type(coordinates))
        print(type(coordinates[0]))
        center_point = [self._get_center_point(coord) for coord in coordinates]
        directions = [self._get_direction(center, image.shape) for center in center_point]
        return directions


    @staticmethod
    def _get_center_point(coord: np.ndarray) -> tuple[int, int]:
        return (coord[0] + coord[2]) / 2, (coord[1] + coord[3]) / 2

    def _get_direction(self, center_point: tuple, image_shape: tuple) -> Direction:
        image_center = (image_shape[0] / 2, image_shape[1] / 2)
        left_right = Direction.LEFT if center_point[0] < image_center[0] else Direction.RIGHT
        up_down = Direction.UP if center_point[1] < image_center[1] else Direction.DOWN
        return Direction.UP
