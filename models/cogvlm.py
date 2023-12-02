from transformers import AutoModelForCausalLM, LlamaTokenizer
import torch
from PIL import Image

GEN_KWARGS = {"max_length": 2048, "do_sample": False}


class CogVLMMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(CogVLMMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CogVLM(metaclass=CogVLMMeta):
    tokenizer: LlamaTokenizer
    model: AutoModelForCausalLM

    def __init__(self):
        self.tokenizer = LlamaTokenizer.from_pretrained("lmsys/vicuna-7b-v1.5")
        self.model = (
            AutoModelForCausalLM.from_pretrained(
                "THUDM/cogvlm-chat-hf",
                torch_dtype=torch.bfloat16,
                low_cpu_mem_usage=True,
                trust_remote_code=True,
            )
            .to("cuda")
            .eval()
        )

    def get_query(self, query: str, image: Image):
        inputs = self._get_inputs_for(query, image)

        with torch.no_grad():
            outputs = self.model.generate(**inputs, **GEN_KWARGS)
            outputs = outputs[:, inputs["input_ids"].shape[1] :]
            return self.tokenizer.decode(outputs[0])

    def _get_inputs_for(self, query: str, image: Image):
        inputs = self.model.build_conversation_input_ids(
            self.tokenizer, query=query, history=[], images=[image]
        )
        inputs = {
            "input_ids": inputs["input_ids"].unsqueeze(0).to("cuda"),
            "token_type_ids": inputs["token_type_ids"].unsqueeze(0).to("cuda"),
            "attention_mask": inputs["attention_mask"].unsqueeze(0).to("cuda"),
            "images": [[inputs["images"][0].to("cuda").to(torch.bfloat16)]],
        }
        return inputs
