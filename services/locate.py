from typing import Optional

import cv2
import numpy as np

from models.grouding_dino import GroundingDino
from schemas.direction import Direction
from services.image import UPLOAD_IMG_DIR


class LocateService:
    grounding_dino: GroundingDino

    def __init__(self):
        self.grounding_dino = GroundingDino()

    def predict(self, img_name: str, class_name: str) -> Optional[list[Direction]]:
        image = cv2.imread(f"{UPLOAD_IMG_DIR}/{img_name}")
        coordinates = self.grounding_dino.predict(class_name, image)
        if not coordinates:
            return None
        center_points = [self._get_center_point(coord) for coord in coordinates]
        directions = [
            self.furthest_direction(image, center_point)
            for center_point in center_points
        ]
        return directions

    @staticmethod
    def _get_center_point(coord: np.ndarray) -> tuple[int, int]:
        return (coord[2] - coord[0]) / 2, (coord[3] - coord[1]) / 2

    @staticmethod
    def distance_from_center(point, center):
        return np.sqrt((point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2)

    def furthest_direction(self, image, point) -> Direction:
        distances = {
            Direction.UP: self.distance_from_center(point, [point[0], 0]),
            Direction.DOWN: self.distance_from_center(
                point, [point[0], image.shape[0] - 1]
            ),
            Direction.LEFT: self.distance_from_center(point, [0, point[1]]),
            Direction.RIGHT: self.distance_from_center(
                point, [image.shape[1] - 1, point[1]]
            ),
        }

        return max(distances, key=distances.get)
