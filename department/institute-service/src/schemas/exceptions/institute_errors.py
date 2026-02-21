class InstituteNotFoundError(Exception):
    def __init__(self, institute_id: int):
        self.institute_id = institute_id
        super().__init__(f"Institute with id '{institute_id}' not found.")