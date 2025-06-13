from . import BaseCRUD

class PodcastCRUD(BaseCRUD):
    def __init__(self, session):
        super().__init__(session)