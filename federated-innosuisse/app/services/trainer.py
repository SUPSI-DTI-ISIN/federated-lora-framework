import torch


class Trainer:

    __DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    def __init__(self):
        print("ok")
