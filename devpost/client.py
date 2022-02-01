from .fetch import get_all_hackathons_pages
from .models import Hackathon, HackathonCollection

class Client: 
    def __init__(self) -> None:
        pass
    
    def get_all_hackathon_pages_as_list(self) -> list:
        self.fetched_hackathons = [Hackathon(h) for h in get_all_hackathons_pages()]
        return self.fetched_hackathons
    
    def get_all_hackathon_pages_as_collection(self) -> HackathonCollection:
        return HackathonCollection(self.get_all_hackathon_pages_as_list())
    