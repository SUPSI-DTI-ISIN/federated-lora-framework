class InferenceRequestError(Exception):
    def __init__(self, detailed_err: str):
        self.detailed_err = detailed_err
        super().__init__(f"Inference request error: {detailed_err}")