class ModelLoadingError(Exception):
    def __init__(self, model_key: str):
        self.model_key = model_key
        super().__init__(f"Error while loading model '{model_key}'.")