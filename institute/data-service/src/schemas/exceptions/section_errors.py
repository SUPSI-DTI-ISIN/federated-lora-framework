class SectionNotFoundError(Exception):
    def __init__(self, section_id: int):
        self.section_id = section_id
        super().__init__(f"Section with id '{section_id}' not found.")