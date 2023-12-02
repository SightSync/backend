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

    def get_intent(self, query: str):
        MESSAGES[1] = {"role": "user", "content": query}
        prompt = self.pipe.tokenizer.apply_chat_template(MESSAGES, tokenize=False, add_generation_prompt=True)
        outputs = self.pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.4, top_k=50, top_p=0.95)
        return outputs[0]["generated_text"]
