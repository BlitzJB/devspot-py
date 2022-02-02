from .fetch import get_all_hackathons_pages
from .models import Hackathon, HackathonCollection

from _thread import start_new_thread
import time
import pickle
import os
from pathlib import Path
from typing import Any, Callable, Sequence
import asyncio


class Client: 
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def async_wrapper(func: Callable[[Any], Any]):
        loop = asyncio.get_event_loop()
        out = loop.run_until_complete(func())
        return out
    
    def get_all_hackathon_pages_as_list(self) -> list:
        self.fetched_hackathons = [Hackathon(h) for h in self.async_wrapper(get_all_hackathons_pages)]
        return self.fetched_hackathons
    
    def get_all_hackathon_pages_as_collection(self) -> HackathonCollection:
        return HackathonCollection(self.get_all_hackathon_pages_as_list())
    
    def create_hackathons_monitor_thread(self, path_to_cache: str, callback: Callable[[Sequence[Hackathon]], None], sleep: int = 120) -> int:
        if path_to_cache.split('.')[-1] not in ['bin', 'bat', 'pkl', 'pickle']: raise TypeError(f"Path to file must be a in ['bin', 'bat', 'pkl', 'pickle'] file formats")
        
        if not Path(path_to_cache).is_file(): 
            now = self.get_all_hackathon_pages_as_collection()
            ids = {hack.id for hack in now.hackathons}
            pickle.dump(ids, open(path_to_cache, 'wb'))
            
        def thread():
            while True:
                hackathons = self.get_all_hackathon_pages_as_collection()
                ids = {hack.id for hack in hackathons.hackathons}
                existing_ids = pickle.load(open(path_to_cache, 'rb'))
                difference = ids - existing_ids
                if not difference: continue
                as_hackathons = hackathons.get_hackathons_by_ids(difference)
                callback(as_hackathons)
                pickle.dump(ids, open(path_to_cache, 'wb'))
                time.sleep(sleep)
        
        return start_new_thread(thread, ())
                