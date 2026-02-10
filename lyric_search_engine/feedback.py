from .storage import SQLiteFeedbackStore

class Feedback:

    def __init__(self, store: SQLiteFeedbackStore):
        self.store = store


    def clicked(self, query: str, doc_id: str):
        self.store.add(query, doc_id, 1.0)

    def skipped(self, query: str, doc_id: str):
        self.store.add(query, doc_id, -0.2)

    def thumbs_up(self, query:str, doc_id:str):
        self.store.add(query, doc_id, 2.0)

    def thumbs_down(self, query: str, doc_id: str):
        self.store.add(query, doc_id, -2.0)