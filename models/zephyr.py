import re

import torch
from transformers import pipeline

MESSAGES = [
    {
        "role": "system",
        "content": "Given there is a user interacting with a blind people virtual assistant that is designed to provide a description about the user environment, I need you to classify the user sentences' intent between:\
1.  General surrounding/environment description/information. Knowing about what items/people/whatever are there in the surroundings. Information about how many items/objects/people/whatever are there.\
2. Specific location of an item (also valid if it's relative to the user).\
3. Information about text/labels.\
 \
The next input will be the sentence that has to be classified. You MUST classify it into one category. In case of doubt, put it in the category that you think fits the most. Don't reason about the answer, just say which category does it belong to. Your answer must be 'GENERAL', 'LOCATION', 'TEXT', or 'UNCERTAIN'. "
                   "Check to make sure your answer is ALWAYS just one of those four words",
    },
    {""}
]


class ZephyrMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ZephyrMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Zephyr(metaclass=ZephyrMeta):
    pipe: pipeline

    def __init__(self):
        self.pipe = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta", torch_dtype=torch.bfloat16,
                             device_map="auto")

    def get_intent(self, query: str) -> str:
        MESSAGES[1] = {"role": "user", "content": query}
        prompt = self.pipe.tokenizer.apply_chat_template(MESSAGES, tokenize=False, add_generation_prompt=True)
        outputs = self.pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.4, top_k=50, top_p=0.95)
        text = outputs[0]["generated_text"]
        return self._get_intent_category_from_response(text)

    @staticmethod
    def _get_intent_category_from_response(response: str) -> str:
        last_newline_index = response.rfind('\n')

        text_after_newline = response[last_newline_index + 1:]

        location_match = re.search(r'\bLOCATION\b', text_after_newline)
        general_match = re.search(r'\bGENERAL\b', text_after_newline)
        text_match = re.search(r'\bTEXT\b', text_after_newline)

        if location_match:
            result = location_match.group()
        elif general_match:
            result = general_match.group()
        elif text_match:
            result = text_match.group()
        else:
            result = "UNCERTAIN"

        return result

    def get_class_for(self, query: str) -> str:
        extract_class_message = [
            {
                "role": "system",
                "content": "Given there is a user interacting with a blind people virtual assistant\
                 that is designed to provide a description about the user environment, I need you to extract the \
                 class name from the user sentence. The class name is the name of the item that the user is asking about. \
                 For example, if the user asks 'Where is the chair?', the class name is 'chair'. \
                If you think the user is not asking about an item or your are not sure about which item is it looking for, just say 'NO CLASS'. Otherwise, ONLY reply with ONE word, the class name.",
            },
            {"role": "user", "content": query},
        ]
        prompt = self.pipe.tokenizer.apply_chat_template(extract_class_message, tokenize=False,
                                                          add_generation_prompt=True)
        outputs = self.pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.4, top_k=50, top_p=0.95)
        text = outputs[0]["generated_text"]
        return self._get_class_from_response(text)

    @staticmethod
    def _get_class_from_response(response: str) -> str:
        last_newline_index = response.rfind('\n')

        text_after_newline = response[last_newline_index + 1:]

        class_match = re.search(r'\b[a-zA-Z]+\b', text_after_newline)

        if class_match:
            result = class_match.group()
        else:
            result = ""

        return result
