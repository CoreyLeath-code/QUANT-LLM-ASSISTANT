import random

def route_model():
    if random.random() < 0.7:
        return "gpt_model_v1"
    return "gpt_model_v2"
