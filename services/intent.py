from models.zephyr import Zephyr


class IntentRecognitionService:
    zephyr: Zephyr

    def __init__(self):
        self.zephyr = Zephyr()

    def get_intent(self, query: str) -> str:
        return self.zephyr.get_intent(query)
