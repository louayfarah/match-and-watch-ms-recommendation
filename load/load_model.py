from transformers import T5Model, T5Tokenizer
import torch

model = T5Model.from_pretrained("t5-small")
tok = T5Tokenizer.from_pretrained("t5-small")
