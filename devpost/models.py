from .fetch import get_all_hackathons_pages

class HackathonCollection:
    def __init__(self, hackathons) -> None:
        if all(isinstance(hackathon, Hackathon) for hackathon in hackathons): self.hackathons = hackathons
        elif all(isinstance(hackathon, dict) for hackathon in hackathons): self.hackathons = [Hackathon(hackathon) for hackathon in hackathons]
        else: raise TypeError(f'HackathonCollection can only be initialized with Hackathon or dict objects')
    
    @staticmethod
    async def now():
        return HackathonCollection(await get_all_hackathons_pages())
    
    def __iter__(self):
        self.__sent_index = 0
        return self
    
    def __next__(self):
        if self.__sent_index == len(self.hackathons): raise StopIteration
        else: self.__sent_index += 1; return self.hackathons[self.__sent_index - 1]
        
    def __len__(self):
        return len(self.hackathons)
    
    def __repr__(self):
        return f'HackathonCollection({len(self.hackathons)})'
    
    def __getitem__(self, index):
        return self.hackathons[index]

    def get_hackathon_by_id(self, id):
        return next(hackathon for hackathon in self.hackathons if hackathon.id == id)
    
    def get_public_hackathons(self):
        return [hackathon for hackathon in self.hackathons if not hackathon.invite_only]
    
    def get(self, filter: dict):
        return [hackathon for hackathon in self.hackathons if all(hackathon.__dict__[key] == value for key, value in filter.items())]

    def get_online_hackathons(self):
        return [hackathon for hackathon in self.hackathons if hackathon.location.lower() == 'online']

class Hackathon: 
    def __init__(self, data) -> None:
        self.id = data.get('id')
        self.title = data.get('title')
        self.location = data.get('displayed_location').get('location')
        self.open_state = data.get('open_state').upper()
        self.thumbnail_url = 'https:' + data.get('thumbnail_url')
        self.url = data.get('url')
        
        # TODO: Convert below strings to datetime objects
        self.submission_periods_string = data.get('submission_period_dates')
        self.time_left_to_submission_string = data.get('time_left_to_submission')
        
        self.themes = [Theme(t) for t in data.get('themes')]
        self.prize_amount = self.cleanup_prize_string(data.get('prize_amount'))
        self.registrations_count = data.get('registrations_count')
        self.featured = data.get('featured')
        self.organization_name = data.get('organization_name')
        self.winners_announced = data.get('winners_announced')
        self.submission_gallery_url = data.get('submission_gallery_url')
        self.start_a_submission_url = data.get('start_a_submission_url')
        self.invite_only = data.get('invite_only') 
        self.eligibility_requirement_invite_only_description = data.get('eligibility_requirement_invite_only_description')
    
    @staticmethod
    def cleanup_prize_string(prize_string: str):
        return float(''.join(ch for ch in prize_string if ch.isdigit() or ch == '.'))

    
    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id

    def _disp(self):
        print('\n\n'); print('-'*50)
        for attr in self.__dict__: print(attr, ':', self.__dict__[attr])
    
class Theme:
    def __init__(self, data) -> None:
        self.id = data.get('id')
        self.name = data.get('name')
        
    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id
