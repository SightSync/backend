from PIL import Image

from models.cogvlm import CogVLM
from services.image import UPLOAD_IMG_DIR


class CaptionService:
    cog_vlm: CogVLM

    def __init__(self):
        self.cog_vlm = CogVLM()

    def get_query(self, img_name: str, query: str) -> str:
        image = Image.open(f"{UPLOAD_IMG_DIR}/{img_name}")
        return self.cog_vlm.get_query(query, image)
